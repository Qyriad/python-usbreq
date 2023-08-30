{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
      inherit (pkgs) python3Packages;

      dependencies = with python3Packages; [
        pyusb
        inflection
      ];

      devDependencies = with python3Packages; [
        sphinx
        sphinx-rtd-theme
      ];

      usbreqPkg = python3Packages.buildPythonPackage {
        pname = "usbreq";
        version = "0.2.1";
        src = ./.;

        format = "pyproject";

        pythonImportsCheck = [ "usbreq" ];

        propagatedBuildInputs = dependencies;
        buildInputs = with python3Packages; [ setuptools wheel ];
      };
    in {

      # IPython is a much nicer development experience.
      devShells.default = pkgs.mkShell {
        propagatedBuildInputs = dependencies ++ devDependencies ++ [ python3Packages.ipython ];
      };

      devShells.minimal = pkgs.mkShell {
        propagatedBuildInputs = dependencies;
      };

      packages.default = usbreqPkg;
    }
  );
}
