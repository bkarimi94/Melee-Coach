const {
    SlippiGame
} = require("@slippi/slippi-js/node");


const game = new SlippiGame(
    "../sample_data/test_game.slp"
);


const settings = game.getSettings();
const stats = game.getStats();


console.log(
    "=== PLAYER SETTINGS ==="
);

console.log(
    JSON.stringify(
        settings,
        null,
        2
    )
);


console.log();

console.log(
    "=== SLIPPI STATS ==="
);

console.log(
    JSON.stringify(
        stats,
        null,
        2
    )
);