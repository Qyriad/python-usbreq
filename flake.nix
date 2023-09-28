{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };

      inherit (builtins) attrValues foldl';
      inherit (pkgs.lib.lists) intersectLists forEach;

      # Like "lib.lists.intersectLists" but takes a list of lists instead of two list arguments.
      intersectAll = foldl' (a: b: a b) intersectLists;

      # Takes a list of packages and returns the intersection of all platforms supported by those packages.
      intersectPlatforms = pkgs: intersectAll (forEach pkgs (pkg: pkg.meta.platforms));

      usbreqDeps = attrValues {
        inherit (pkgs.python3Packages)
          pyusb
          inflection
        ;
      };

      usbreq = pkgs.python3Packages.buildPythonPackage rec {
        pname = "usbreq";
        version = "0.2.1";
        format = "pyproject";
        src = ./.;

        meta = {
          description = "A USB library for humans";
          #platforms = intersectPlatforms (with pkgs.python3Packages; [ pyusb inflection ]);
          platforms = intersectPlatforms usbreqDeps;
        };

        pythonImportsCheck = [ "usbreq" ];

        propagatedBuildInputs = usbreqDeps;

        nativeBuildInputs = attrValues {
          inherit (pkgs.python3Packages)
            setuptools
            wheel
          ;
        };

        # I guess documentation builders are check inputs?
        nativeCheckInputs = attrValues {
          inherit (pkgs.python3Packages)
            sphinx
            sphinx-rtd-theme
          ;
        };
      };

    in {
      packages.default = usbreq;

      devShells.default = pkgs.mkShell {

        inputsFrom = [ usbreq ];

        packages = attrValues {
          inherit (pkgs.python3Packages)
            build
            twine
            # IPython is a much nicer development experience.
            ipython
          ;
        } ++ [
          pkgs.pyright
        ];

      };

    }

  );
}
