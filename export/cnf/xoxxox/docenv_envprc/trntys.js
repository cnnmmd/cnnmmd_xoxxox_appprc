process.stdout.write(require("typescript").transpile(require("fs").readFileSync(0, "utf8")))
