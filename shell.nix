with (import <nixpkgs> {});
mkShell rec {
  buildInputs = [
    python311
    stdenv.cc.cc.lib
    libz
    xorg.libxcb
    xorg.libSM
    xorg.libICE
    libGL
    libGLU
    glib
    liblo
  ];

  LD_LIBRARY_PATH = lib.makeLibraryPath buildInputs;

  shellHook = ''
  '';
}
