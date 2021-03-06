from codeword import codeword, constants


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.echo-sdk-ams.app.c00ae347-78bf-4165-a1b1-6f302b5c6180"):
        raise ValueError("Invalid Application ID")

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    with codeword.get_connection(constants.DB_PATH) as conn:
        current_codeword = codeword.get_codeword(conn)
        print("current_codeword: %s" % (current_codeword, ))

    # Dispatch to your skill's launch
    return get_codeword_response(current_codeword)


def get_codeword_response(current_codeword):
    session_attributes = {}
    speech_output = current_codeword
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please try again by saying 'Alexa, ask codeword'"
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(output, reprompt_text):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'Your code phrase',
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': True
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }