{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
      };
    in {
      devShells.default = pkgs.mkShellNoCC {
        packages = with pkgs; [
          python3
        ];

        shellHook = ''
          echo "Welcome to the dev-shell!"
        '';
      };
    });
}
