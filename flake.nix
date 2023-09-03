{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };

      intersectLists = pkgs.lib.lists.intersectLists;
      forEach = pkgs.lib.lists.forEach;

      # Like "lib.lists.intersectLists" but takes a list of lists instead of two list arguments.
      intersectAll = builtins.foldl' (a: b: a b) intersectLists;

      # Takes a list of packages and returns the intersection of all platforms supported by those packages.
      intersectPlatforms = pkgs: intersectAll (forEach pkgs (pkg: pkg.meta.platforms));

      usbreq = pkgs.python3Packages.buildPythonPackage rec {
        pname = "usbreq";
        version = "0.2.1";
        format = "pyproject";
        src = ./.;

        meta = {
          description = "A USB library for humans";
          platforms = intersectPlatforms (with pkgs.python3Packages; [ pyusb inflection ]);
        };

        pythonImportsCheck = [ "usbreq" ];

        propagatedBuildInputs = with pkgs.python3Packages; [
          pyusb
          inflection
        ];

        nativeBuildInputs = with pkgs.python3Packages; [
          setuptools
          wheel
        ];

        # I guess documentation builders are check inputs?
        nativeCheckInputs = with pkgs.python3Packages; [
          sphinx
          sphinx-rtd-theme
        ];
      };

      devShellPkgs = with pkgs.python3Packages; [
        build
        twine
        ipython
      ];

    in {
      packages.default = usbreq;

      # IPython is a much nicer development experience.
      devShells.default = pkgs.mkShell {

        inputsFrom = [ usbreq ];

        packages = devShellPkgs;

      };

      devShells.lsp = pkgs.mkShell {
        meta.description = "Like devShells.default, but with Pyright.";

        inputsFrom = [ usbreq ];

        packages = devShellPkgs ++ [
          pkgs.pyright
        ];

      };

    }

  );
}
