# pytff
Wrapper arround Kovacs's Template Fourier Fitting

## Setup

In all cases you need to download and compile
[Template Fourier Fitting](http://www.konkoly.hu/staff/kovacs/tff.html) the
parameters file (`tff.par`) and  the Template Fourier decompositions file
(`template.dat`) are not necesary.

You can compile the `tff.f` with the command

```bash
$ gfortran tff.f -o tff
```

### Basic Install

Execute

```bash
$ pip install pytff
```

or

```bash
$ easy_install pytff
```

### Development Install

1.  Clone this repo and then inside the local
2.  Execute

    ```bash
    $ pip install -e .
    ```

    or

    ```bash
    $ python setup.py develop
    ```






