# passcraker
A simple password craker.

## How to use

```shell script
usage: passcraker.py [-h] [--threads THREADS] [--queue_size QUEUE_SIZE]
                     dictionary password

positional arguments:
  dictionary            The dictionary file you want to use to crack password
  password              The victim password file

optional arguments:
  -h, --help            show this help message and exit
  --threads THREADS     The number of running threads when cracking passwords
  --queue_size QUEUE_SIZE
                        The maximum size of the queue
```

### Example
```shell script
chmod +x passcraker.py
# Set parallel threads to 50 and set queue size to 200.
./passcraker <dict_file> <passwords_file> --threads 50 --queue_size 200
```
