{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };
  # FIXME: add a package output too
  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.default = pkgs.mkShell {
        propagatedBuildInputs = with pkgs.python3Packages; [
          pyusb
          inflection
          ipython
        ];
      };
    }
  );
}
