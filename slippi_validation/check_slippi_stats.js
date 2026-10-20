const path = require("path");

const {
    SlippiGame
} = require("@slippi/slippi-js/node");


if (process.argv.length !== 3) {
    console.log(
        "Usage:"
    );

    console.log(
        "node check_slippi_stats.js " +
        "path/to/replay.slp"
    );

    process.exit(1);
}


const replayPath = path.resolve(
    process.argv[2]
);


const game = new SlippiGame(
    replayPath
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
    "=== OPENING TYPES ==="
);


const openingTypes = (
    stats.conversions.map(
        conversion => {
            const firstMove = (
                conversion.moves.length > 0
                    ? conversion.moves[0]
                    : null
            );

            return {
                defenderIndex:
                    conversion.playerIndex,

                attackerIndex:
                    firstMove
                        ? firstMove.playerIndex
                        : null,

                startFrame:
                    conversion.startFrame,

                endFrame:
                    conversion.endFrame,

                openingType:
                    conversion.openingType,

                didKill:
                    conversion.didKill
            };
        }
    )
);


console.log(
    JSON.stringify(
        openingTypes,
        null,
        2
    )
);


console.log();


console.log(
    "=== OVERALL STATS ==="
);


const overallStats = (
    stats.overall.map(
        player => {
            return {
                playerIndex:
                    player.playerIndex,

                conversionCount:
                    player.conversionCount,

                killCount:
                    player.killCount,

                openingsPerKill:
                    player.openingsPerKill,

                neutralWinRatio:
                    player.neutralWinRatio,

                counterHitRatio:
                    player.counterHitRatio,

                beneficialTradeRatio:
                    player.beneficialTradeRatio
            };
        }
    )
);


console.log(
    JSON.stringify(
        overallStats,
        null,
        2
    )
);