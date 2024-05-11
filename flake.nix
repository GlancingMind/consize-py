{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      consize-py = with pkgs.python3Packages; buildPythonApplication {
        pname = "consize-py";
        version = "1.0";
        propagatedBuildInputs = [
          requests
          requests-file
        ];
        src = ./.;
      };
    in {
      packages.default = consize-py;
    });
}
