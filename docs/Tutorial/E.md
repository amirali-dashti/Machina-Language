# E command

E command is used to define the collection of transitions between two states aka. the Sigma.

To use E, run this:

```
E.{
q<i> q<j> <transition>
q<j> q<k> <transition>
.
.
.
}
```

> [!TIP]
> If you want to add relations one by one, use ```Q.label.add.q<i> q<j> <transition>```. see [here](https://github.com/devtracer/Machina-Language/blob/main/docs/Tutorial/Q.md) for more.

> [!TIP]
> To edit and or remove any transition, you'll need Q commands. see [here](https://github.com/devtracer/Machina-Language/blob/main/docs/Tutorial/Q.md) for more.
