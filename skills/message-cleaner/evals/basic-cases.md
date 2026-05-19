# Message Cleaner Basic Eval Cases

These cases are used to manually validate whether the message-cleaner skill behaves correctly.

## Case 1: Messy deployment message

Input:

hey can u check the deploy thing idk if prod is broken but logs look weird maybe ask alex

Expected qualities:

- Mentions Alex
- Mentions deployment
- Mentions unusual/weird logs
- Does not invent extra technical details
- Sounds clear and natural
- Keeps the message concise

## Case 2: Short reminder

Input:

need everyone to fill timesheet today dont forget pls

Expected qualities:

- Mentions timesheet
- Mentions today
- Sounds polite
- Stays short
- Does not add unnecessary details

## Case 3: Firm but respectful

Input:

tell them they need to send the report before 5 or we cant move forward

Expected qualities:

- Mentions the report
- Mentions before 5
- Mentions that work cannot move forward without it
- Sounds firm but respectful
- Does not sound aggressive

## Case 4: Less corporate tone

Input:

please make this less corporate: "Kindly be advised that your response is required at your earliest convenience"

Expected qualities:

- Sounds more natural
- Keeps the original ask
- Removes overly formal/corporate wording