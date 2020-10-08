
pip3 install -r requirements.txt --target ./package --upgrade
cd package
zip -r9 ${OLDPWD}/terminal.zip .
cd ${OLDPWD}
rm -r package
zip -r9 ./terminal.zip .
aws lambda update-function-code --function-name "FenixTerminal" --zip-file fileb://terminal.zip
rm terminal.zip