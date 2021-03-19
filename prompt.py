import PyInquirer as inquirer


def choose(message: str, choices: list):
    questions = [
        {
            'type': 'list',
            'name': 'question',
            'message': message,
            'choices': choices
        }
    ]

    promptUser = inquirer.prompt(questions)['question']
    return promptUser
