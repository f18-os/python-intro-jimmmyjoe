# Shell Lab

## Instructions

Both shel-basic.py and shel.py should be executable, so usage
should be as simple as

```
/<path>/shel-basic.py .
```

## Note

While attempting to complete the graduate requirements for this
lab, I ran into some issues with forking multiple times.
Therefore, shel-basic.py will satisfy the undergraduate
requirements until I can finish shel.py .

Pipe functionality tested with

```
ls | grep s
```

and

```
ls | wc
```

In both test cases, a C-c C-d is needed to terminate file. I
expect this to be a missing EOF indicator but have been unable
to figure out where to inject it.. I lose control once I exec..