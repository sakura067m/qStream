from setuptools import setup

requirements = [
    "slackclient>=1.3.1",
    "PyQt5>=5.8.2",  # TBD
]

setup(
    name="qStream",  # TBC
    version="1.0.0",
    description="show your stream. Slack version",
    url="https://github.com/sakura067m/qStream",
    author="sakura067m",
    author_email="3IE19001M@s.kyushu-u.ac.jp",
##    license='',  # TBD
    packages=["qStream"],
    package_dir={"qStream": "qStream"},
    package_data={
        "qStream"=[]
    },
    entry_points={
        "gui_scripts": ["qStream = qStream.__main__:RTMStreamer.go"]
    },
    install_requires=requirements,
    keywords="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Communications :: Chat",
    ],
)

# we need a SLACK_LEGACY_TOKEN
print("""\
please set your SLACK_LEGACY_TOKEN to your os.environ["SLACK_LEGACY_TOKEN"].
you can do that everytime you run this app in a shell or save it to the settings. 
this token will let the app to recieve your workspace's RTMs.
thank you.""")