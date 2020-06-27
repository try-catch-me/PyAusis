from plugin import plugin, require
import requests


@require(network=True)
@plugin('quiz')
class trivia:
    errCode = "An error occurred. Please try again later."
    """
    Usage: Type trivia and follow the instructions.
    This plugin gives you trivia questions (mcq or true/false)
    for you to test your trivia knowledge
    """

    def __call__(self, ausis, s):
        trivia_fetch = self.get_trivia(ausis)
        question_type = trivia_fetch["results"][0]["type"]
        options = trivia_fetch["results"][0]["incorrect_answers"]
        if trivia_fetch is not None:
            if(question_type == "multiple"):
                self.mcq_question(ausis, trivia_fetch)
            else:
                self.true_false_question(ausis, trivia_fetch)

    def get_trivia(self, ausis):
        """
        function creates request to api and fetches the corresponding data
        """
        url = "https://opentdb.com/api.php?amount=1"
        r = requests.get(url)
        return r.json()

    def true_false_question(self, ausis, trivia_fetch):
        response_code = trivia_fetch["response_code"]
        if (response_code != 0):
            ausis.say(errCode)
            return
        else:
            question = trivia_fetch["results"][0]["question"]
            question = question.replace("&quot;", "\"")
            ausis.say("True/False: " + question)
            options = ["true", "false"]
            correct = trivia_fetch["results"][0]["correct_answer"]
            correct = correct.lower()
            self.true_false_answer(ausis, options, correct)

    def true_false_answer(self, ausis, options, correctAnswer):
        answerPrompt = "Please enter either \'true\' or \'false\'"
        answer = (ausis.input(answerPrompt + "\n")).lower()
        while answer not in options:
            ausis.say("Invalid option")
            answer = (ausis.input(answerPrompt + "\n")).lower()
        if (answer == correctAnswer):
            ausis.say("Correct!!")
        else:
            ausis.say("Sorry, that's incorrect")

    def mcq_question(self, ausis, trivia_fetch):
        response_code = trivia_fetch["response_code"]
        if (response_code != 0):
            ausis.say(errCode)
            return
        else:
            question = trivia_fetch["results"][0]["question"]
            question = question.replace("&quot;", "\"")
            question = question.replace('&#039;', "'")
            ausis.say("Multiple Choice: " + question)
            options = trivia_fetch["results"][0]["incorrect_answers"]
            correct_answer = trivia_fetch["results"][0]["correct_answer"]
            options.append(correct_answer)
            options.sort()
            option_count = 0
            answersDict = {}
            for option in options:
                option_count = option_count + 1
                answersDict[str(option_count)] = option
                ausis.say(str(option_count) + ". " + option)
            self.mcq_answer(ausis, answersDict, correct_answer, option_count)
        return

    def mcq_answer(self, ausis, answersDict, correctAnswer, maxCount):
        answerPrompt = "Please enter an integer 1-" + str(maxCount)
        answer = ausis.input(answerPrompt + "\n")
        while answer not in answersDict.keys():
            ausis.say("Invalid option")
            answer = ausis.input(answerPrompt + "\n")
        userAnswer = answersDict[answer]
        if (userAnswer == correctAnswer):
            ausis.say("Correct!!")
        else:
            ausis.say("Sorry, the correct answer was " + correctAnswer)
