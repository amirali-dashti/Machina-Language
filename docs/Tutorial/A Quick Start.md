# A Quick Start

This page guides you to the very beginning of the Machina Language programming.

To define your DFA, you must follow the order bellow. Mathematically, The set of states exist before defining relations. Therefore is Machina.

> [!WARNING]
> Using different order may lead to errors.

### 1. States

We start with defining states. You can define states in this way: 
```
Q.len = <THE AMOUNT OF STATES>
```
You can see the states with this command:
```
Q.print.states
```
The output should look like this:
```
  Name Is_Start Is_Final
0   q1     True    False
1   q2    False     True
```
> [!TIP]
> You can change the Start/Final booleans of states with ```Q.changestate.<name> <is start boolean> <is final boolean>```. see [Here] for more.

### 2. Transitions

There are two approaches in adding a transition between two states:
  - Add the transitions altogether:
    ```
    E.{
    q<i> q<j> <transition>
    q<j> q<k> <transition>
    .
    .
    .
    }
    ```
  - Add the transitions one by one:
    ```
    Q.label.add.q<i> q<j> <transition>
    ```
> [!TIP]
> Edit two states' transitions with ```Q.label.change.q<i> q<j> <transition>```. see [Here] for more.

> [!TIP]
> Remove two states' transitions with ```Q.label.remove.q<i> q<j> <transition>```. see [Here] for more.

To have access and see to transitions, use:
```
Q.print.tra
```
The output should look like this:
```
  Start_State End_State Label
0          q1        q1     a
1          q1        q2     b
2          q2        q2   aUb
3          q1        q2     e
```

### 3. Use ```do``` functions to work with the DFA

We're done with defining our DFA. now you can use the ```do``` methods to work on your DFA. see [Here] for more.
