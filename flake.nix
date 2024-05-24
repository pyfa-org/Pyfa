{
  description = "Nix Flake for Pyfa";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    {
      formatter.x86_64-linux = nixpkgs.legacyPackages.x86_64-linux.nixfmt-rfc-style;

      ##### x86_64-linux #####
      packages.x86_64-linux = {
        pyfa =
          let
            pkgs = import nixpkgs { system = "x86_64-linux"; };
            name = "pyfa";
            version = "v2.58.3";
            src = pkgs.fetchurl {
              url = "https://github.com/pyfa-org/Pyfa/releases/download/${version}/pyfa-${version}-linux.AppImage";
              sha256 = "opzZSiVWfJv//KONocL9byZKqX/hWkPU+ssdceUDXh0=";
            };
          in
          pkgs.appimageTools.wrapType2 { inherit name version src; };

        default = self.packages.x86_64-linux.pyfa;
      };
      apps.x86_64-linux = {
        pyfa = {
          type = "app";
          program = "${self.packages.x86_64-linux.pyfa}/bin/pyfa";
        };

        default = self.apps.x86_64-linux.pyfa;
      };
    };
}
