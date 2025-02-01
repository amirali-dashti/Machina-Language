# Q commands

Commands that's started with "Q" are those that are related to the machine's states and does functions like defining, defining and editing the said states.

Here is the list of Q commands:

| Exlanation  | Syntax |
| ------------- | ------------- |
| Set and create states  | ```Q.len = <integer number>```  |
| Preview states  | ```Q.print.states```  |
| Preview transitions | ```Q.print.tra``` |
| Add label to two states | ```Q.label.add.q<i> q<j> <label>``` |
| Edit label of two states | ```Q.label.change.q<i> q<j> <label>``` |
| Remove label from two states | ```Q.label.remove.q<i> q<j> <label>``` |
| Change a state's status from being the start and the final state | ```Q.changestate.q<i> <being start BOOLEAN> <being final BOOLEAN>``` |
