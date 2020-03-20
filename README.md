# wirvsvirus-telefonassistent

## Speech libraries
| Type               | Provider      | Price      | Link
| -------------------|:-------------:| -----------| ----- |
| Speech to text     | Google        | Free < 60m |
| Speech to text     | Microsoft     | Free < 5h  |
| Speech to text     | Uni Hamburg   | Free OP    | https://github.com/uhh-lt/kaldi-tuda-de#pretrained-models
|--------------------|               |            |
| Text to speech     | Google        | Free       | https://pypi.org/project/gTTS/

## After cloning
1) cd into directory
2) docker build -t assistent .
3) sudo docker run -it --rm --name assistent assistent
