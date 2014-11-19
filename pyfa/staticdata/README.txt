Generating a new sqlite dump HOWTO

You'll need pyfa itself (git://dev.evefit.org/pyfa.git)
as well as phobos (git://dev.evefit.org/phobos.git)

Phobos can dump the whole of the eve cache to json, after installing it (=python setup.py install) just do python dumpToJson.py -e /path/to/eve -c /path/to/eve/cache -s serverName -o /output/folder

Arguments explained: -e and -c should be pretty self explanitory, they're the path to the eve install and the eve cache respectivly

-s is the serverName, its used to figure out which subfolder in the machonet folder we're intrested in. (possible values: tranquility, singularity, duality).
This is passed directly to reverence which keeps a serverName to IP address mapping. You could probably add more servers with their IPs in the reverence sourcecode (cache.py file, around like 150 in the CacheMgr class) if you need another one.

-o is the output folder to dump all json files to, it should already exist or you'll get errors.



After thats done, you'll have all json files you need, and you can use a script within pyfa to generate a dump from that.

After you checked out pyfa, don't forget to update submodules (git submodule update --init).

and then browse to eos/utils/scripts/jsonToSql.py, which can generate the sqlite dump pyfa needs.

python jsonToSql.py -d eve.db -j /output/folder

Once thats done, you should have a nice little sqlite database, you can replace the one in the staticdata folder with yours and it should run right away.