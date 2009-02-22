// Compile with mtasc:
//   mtasc -version 9 -swf DecryptPid.swf -main -header 20:20:1 DecryptPid.as

class DecryptPid {
    var pid:String;

    function DecryptPid() {
    }

    function decrypt(pid:String) {
        this.pid = pid;
        var loader:MovieClipLoader = new MovieClipLoader();
        loader.addListener(this);
        var sec:MovieClip = _root.createEmptyMovieClip("sec", 10)
        sec._lockroot = true;
        loader.loadClip("http://www.hulu.com/sec.swf", sec);
    }

    function onLoadInit(sec:MovieClip) {
        var s:String = sec.dec(this.pid);
        trace("hulupid=" + s)
    }

    static function main(mc) {
        (new DecryptPid()).decrypt(_root.pid);
    }
}
