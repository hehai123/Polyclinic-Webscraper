import SendEmail


def formatContent(slots):
    if not slots:
        return

    slotCount = 0
    locationCount = 0
    content = ''
    html = '''
        <!DOCTYPE html>
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your HTML Title</title>
        <body>
    '''

    for locations in slots.keys():
        locationCount += 1
        content += locations + '\n'
        html += '<b><u>' + locations + '</b></u>' + '<br>'
        for slot in slots[locations]:
            slotCount += 1
            slotTime = slot.split(',', 2)
            content += slotTime[1] + '\n'
            html += slotTime[1] + '<br>'
        content += '\n'
        html += '<br>'
    html += '''
        </body>
        </html>
    '''

    if slotCount == 1:
        if locationCount == 1:
            subject = str(slotCount) + ' appointment slot found at 1 location!'
        else:
            subject = str(slotCount) + ' appointment slot found at ' + \
                str(locationCount) + ' locations!'
    else:
        if locationCount == 1:
            subject = str(slotCount) + \
                ' appointment slots found at 1 location!'
        else:
            subject = str(slotCount) + ' appointment slots found at ' + \
                str(locationCount) + ' locations!'

    SendEmail.sendMail(subject, content, html)
