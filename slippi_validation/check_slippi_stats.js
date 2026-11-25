// Print Slippi's reference statistics for a single replay.
const path = require("path");
const { SlippiGame } = require("@slippi/slippi-js/node");

if (process.argv.length !== 3) {
    console.log("Usage: node check_slippi_stats.js path/to/replay.slp");
    process.exit(1);
}

const replayPath = path.resolve(process.argv[2]);
const game = new SlippiGame(replayPath);
const stats = game.getStats();

console.log("=== PLAYER SETTINGS ===");
console.log(JSON.stringify(game.getSettings(), null, 2));

console.log("=== OVERALL STATISTICS ===");
for (const player of stats.overall || []) {
    console.log(JSON.stringify({
        playerIndex: player.playerIndex,
        conversionCount: player.conversionCount,
        killCount: player.killCount,
        openingsPerKill: player.openingsPerKill,
        neutralWinRatio: player.neutralWinRatio,
        counterHitRatio: player.counterHitRatio,
    }, null, 2));
}

console.log("=== CONVERSION TYPES ===");
for (const conversion of stats.conversions || []) {
    console.log(JSON.stringify({
        defenderIndex: conversion.playerIndex,
        startFrame: conversion.startFrame,
        endFrame: conversion.endFrame,
        openingType: conversion.openingType,
        didKill: conversion.didKill,
    }));
}
