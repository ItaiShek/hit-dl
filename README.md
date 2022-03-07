<!-- Badges -->
[![](https://img.shields.io/github/v/release/ItaiShek/hit-dl)](https://github.com/ItaiShek/hit-dl/releases)
![](https://img.shields.io/github/downloads/ItaiShek/hit-dl/total?color=red)
[![](https://img.shields.io/github/issues/ItaiShek/hit-dl?color=yellow)](https://github.com/ItaiShek/hit-dl/issues)
[![](https://img.shields.io/github/license/ItaiShek/hit-dl?label=license&color=green)](https://github.com/ItaiShek/hit-dl/blob/main/LICENSE)

# General info

hit-dl is a software meant for HIT students, to download an entire course from moodle for offline reading.

## Usage
```
usage: hit-dl -u USERNAME -p PASSWORD URL [URL1 URL2...]

 e.g.: hit-dl -u student -p pass123 https://md.hit.ac.il/course/view.php?id=12345

positional arguments:
  URL                     the course/s url/s you want to download

optional arguments:
  -h, --help              show this help message and exit
  -u, --username          your moodle username
  -p, --password          your moodle password
  -v, --verbose           print debugging information
  -r, --robots-txt        disobey ROBOTS.txt
  -a, --user-agent        override the default user agent
  -c, --cookies-disabled  disable cookies
```

## Installation

<details>

<summary style="font-size:large">Linux</summary>

#### Method 1: Using curl 

```bash
sudo curl -L https://github.com/ItaiShek/hit-dl/releases/download/v1.0.0/hit-dl -o /usr/local/bin/hit-dl
sudo chmod a+rx /usr/local/bin/hit-dl
```

#### Method 2: Using wget

```bash
sudo wget https://github.com/ItaiShek/hit-dl/releases/download/v1.0.0/hit-dl -O /usr/local/bin/hit-dl
sudo chmod a+rx /usr/local/bin/hit-dl
```

#### Method 3: Direct download

Download it from [here](https://github.com/ItaiShek/hit-dl/releases/download/v1.0.0/hit-dl).

#### Method 4: Clone repository

Requires: python >= 3.6

```bash
git clone https://github.com/ItaiShek/hit-dl.git && cd hit-dl
python -m pip install -r requirements.txt
```

</details>


<details>

<summary style="font-size:large">Windows</summary>

#### Direct download

Download it from [here](https://github.com/ItaiShek/hit-dl/releases/download/v1.0.0/hit-dl.exe).

Add the file to any folder except "C:\Windows\System32", and add it to [PATH](https://docs.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)).

</details>


