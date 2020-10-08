import json
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

import helpers



class Job:
    def __init__(self, config):
        self.config = config


    def run_job(self):
        return


class FenixJob(Job):
    def __init__(self, config):
        super().__init__(config)
        self._dateFormat = '%A, %B %d, %Y'
        self._shiftMatch = '.*Shift'
        self._lineName = 'LINE'
        self._excludes = set(['LINE', 'REEFERS', 'SPECIAL EQUIPMENT'])
        self._openName = 'OPEN'
        self._closeName = 'CLOSED'


    def get_date(self, cr, offset):
        newOffset = offset
        for line in cr[offset:]:
            newOffset += 1
            if any(line):
                try:
                    date = datetime.strptime(line[0], self._dateFormat)
                    return {'data': date, 'offset': newOffset}
                except:
                    continue

        return None


    def get_shift(self, cr, offset):
        newOffset = offset
        for line in cr[offset:]:
            newOffset += 1
            if any(line):
                if re.match(self._shiftMatch, line[0]):
                    shift = line[0][0]
                    return {'data': shift, 'offset': newOffset}

        return None


    def get_items(self, cr, offset):
        newOffset = offset
        sline = None
        for line in cr[offset:]:
            newOffset += 1
            if any(line) and line[0] == self._lineName:
                sline = line
                break

        if sline == None:
            return None

        items = []
        for _ in range(2):
            for elem in sline:
                if elem != '' and elem not in self._excludes:
                    items.append(elem)   

            sline = cr[newOffset]

        newOffset += 1

        return {'data': items, 'offset': newOffset}


    def get_lines(self, cr, offset):
        newOffset = offset
        lines = []
        for line in cr[offset:]:
            if any(line):
                lines.append(line[0])
            else:
                break

        return {'data': lines, 'offset': newOffset}


    def get_values(self, cr, offset):
        newOffset = offset
        line = cr[offset]
        newOffset += 1

        values = list(map(lambda x: True if x == self._openName else (False if x == self._closeName else None), line[1:]))

        return {'data': values, 'offset': newOffset}


    def get_schedule(self, cr, date, offset):
        data = self.get_shift(cr, offset)

        if data == None:
            return None

        shift = data['data']
        offset = data['offset']

        data = self.get_items(cr, offset)
        items = data['data']
        offset = data['offset']

        data = self.get_lines(cr, offset)
        slines = data['data']
        offset = data['offset']

        lines = []
        for sline in slines:
            line = {'name': sline, 'items': []}

            data = self.get_values(cr, offset)
            values = data['data']
            offset = data['offset']

            if len(values) != len(items):
                continue

            for i in range(len(items)):
                line['items'].append({'name': items[i], 'status': values[i]})

            lines.append(line)

        result = {
            'date': date,
            'shift': shift,
            'lines': lines
        }

        return {'data': result, 'offset': offset}


    def get_schedules(self, cr, offset):
        data = self.get_date(cr, offset)

        if data == None:
            return None
        
        date = data['data']
        offset = data['offset']
        
        schedules = []

        data = self.get_schedule(cr, date, offset)

        if data != None:
            schedules.append(data['data'])
            offset = data['offset']

            data = self.get_schedule(cr, date, offset)
            if data != None:
                schedules.append(data['data'])
                offset = data['offset']

        return {'data': schedules, 'offset': offset}


    def run_job(self):
        target = self.config['target']

        page_content = helpers.download_page_content(self.config['mainUrl'], target)
        soup = BeautifulSoup(page_content, 'html.parser')

        gsheeturl = urlparse(soup.body.find('iframe')['src'])
        gsheeturl = gsheeturl._replace(path=gsheeturl.path[:-4], query='output=csv')

        cr = helpers.download_csv_content(gsheeturl.geturl(), target)

        timestamp = datetime.utcnow().timestamp() * 1000

        allSchedules = []
        offset = 0
        while True:
            data = self.get_schedules(cr, offset)
            
            if data == None:
                break

            schedules = data['data']
            offset = data['offset']
            
            for schedule in schedules:
                schedule['terminal'] = target
                schedule['timestamp'] = timestamp

            allSchedules += schedules
            
        return allSchedules
