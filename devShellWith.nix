{ withPkgs, cwd }:
let
  sys = builtins.currentSystem;
  flake = builtins.getFlake cwd;
  pkgs = import flake.inputs.nixpkgs {};
  qyriad = import (builtins.getFlake "github:Qyriad/dotfiles") {};
  withEnv = {
    nixpkgs = pkgs;
    qyriad = qyriad.packages.${sys};
  };
in
  flake.devShells.${sys}.default.overrideAttrs (final: prev: {
    propagatedBuildInputs = [ qyriad.packages.${builtins.currentSystem}.xonsh ];
  })
