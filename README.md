# codeword-alexa-skill

Generate code words using Alexa.

## How to deploy

-   Install nltk (`conda install nltk`), then run the NLTK downloader:

```
python -c 'import nltk; nltk.download()'
```

-   Install `averaged_perceptron_tagger`
    Install the `wordnet` corpus.
-   Run the following to generate the words database:

```
cd codeword
./generate_lookup.py
```

Then create a deployment ZIP file for lambda:

```
./create_lambda_deployment
```

## How to set up Lambda

-   Create a Lambda deployment ZIP file
-   Create a new Lambda function
    -   Handler: "main.lambda_handler"
    -   Role: "lamda_basic_execution"
    -   Event source: "Alexa Skills Kit"
-   You can test it with the following basic event:

```
{
  "session": {
    "new": true,
    "sessionId": "session1234",
    "attributes": {},
    "user": {
      "userId": null
    },
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.[unique-value-here]"
    }
  },
  "version": "1.0",
  "request": {
    "type": "LaunchRequest",
    "requestId": "request5678"
  }
}
```

-   Now go to https://developer.amazon.com/edw/home.html#/skills/list
-   Create a new skill
    -   Name: "Code Phrase Generator"
    -   Invocation name: "for a code phrase"
    -   Version: "1.0"
    -   Endpoint: Lambda ARN
    -   The intent schema is:

```
{
    "intents": [
        {
            "intent": "GetCodePhrase"
        }
    ]
}
```

    -   Sample utterances:

```
GetCodePhrase for a code phrase
GetCodePhrase for a phrase
GetCodePhrase for a code
GetCodePhrase for a code word
GetCodePhrase for a codeword
```
