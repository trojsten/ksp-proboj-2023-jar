package main

const MinX = -1000
const MaxX = 1000
const MinY = -1000
const MaxY = 1000
const WorldSizeShrink = 4
const MinWorldSize = 100
const ShrinkWorldAfter = 500
const SpawnIterations = 10
const TankLevelUpdateFreq = 10
const PlayerEntityCollisionHealth = 10

var PlayerOutOfWorldHealth = 15

const BiggerPlayerOutOfWorldHealth = 30
const IncreaseOutOfWorldKill = 3000
const EntityHitExpCoefficient = 0.3
const EntityCollisionExpCoefficient = 0.3
const PlayerHitExpCoefficient = 0.5
const PlayerCollisionExpCoefficient = 0.5
const BulletCollisionTTL = 1
const MaxRespawn = 3
const EntitiesInitSpawnNumber = 20
const MaxEntitySpawnProb = 0.2
const MaxEntityRadius = 30
const MinEntityRadius = 20
const MaxEntityHealth = 100
const FractionOfPlayerSpeedToBullet = 0.95
const KillPlayerExp = 5000
const KillEntityExp = 5000
const DiedOrderConstant = 5000
const DiedOrderPower = 1.5
const MaxEntitiesCount = 20000
