import inquirer

async def get_user_selection(topic, message, choices):
    question = [
        inquirer.List(
            topic,
            message,
            choices,
        )
    ]
    selections = inquirer.prompt(question)
    selection = selections[topic]

    return selection