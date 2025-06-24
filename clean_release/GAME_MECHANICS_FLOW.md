# 🎮 Jungle Drive - Game Mechanics Flow Chart

## 🚗 **Player Action Flow Diagram**

```
                              PLAYER INPUT
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │    MENU     │ │   GAMEPLAY  │ │   SPECIAL   │
            │ NAVIGATION  │ │   CONTROLS  │ │   ACTIONS   │
            └─────────────┘ └─────────────┘ └─────────────┘
                    │              │              │
                    ▼              ▼              ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │ ↑↓ Navigate │ │ → Accelerate│ │  P Pause    │
            │ ENTER Select│ │ ← Brake     │ │ ESC Menu    │
            │             │ │ ↑ Jump      │ │ R Restart   │
            │             │ │ ↓ Fast Drop │ │             │
            └─────────────┘ └─────────────┘ └─────────────┘
                    │              │              │
                    └──────────────┼──────────────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │  GAME RESPONSE  │
                         └─────────────────┘
```

## ⚡ **Jeep Physics & Movement Flow**

```
                              JEEP MOVEMENT CYCLE
                                      │
                                      ▼
                            ┌─────────────────┐
                            │  INPUT READING  │
                            │                 │
                            │ keys_pressed =  │
                            │ pygame.key.     │
                            │ get_pressed()   │
                            └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ FORCE CALCULATION│
                            │                 │
                            │ → Right: +accel │
                            │ ← Left:  -accel │
                            │ ↑ Jump: -15 vel │
                            │ ↓ Fast: +2 grav │
                            └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ PHYSICS UPDATE  │
                            │                 │
                            │ velocity_x +=   │
                            │ acceleration    │
                            │ velocity_y +=   │
                            │ gravity (0.8)   │
                            └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ POSITION UPDATE │
                            │                 │
                            │ x += velocity_x │
                            │ y += velocity_y │
                            │ Apply friction  │
                            │ (0.85 factor)   │
                            └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ COLLISION CHECK │
                            │                 │
                            │ • Terrain       │
                            │ • Obstacles     │
                            │ • Boundaries    │
                            └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ RESOURCE UPDATE │
                            │                 │
                            │ Fuel -= 0.04    │
                            │ (when moving)   │
                            │ Health check    │
                            └─────────────────┘
```

## 🎯 **Smart Collision System Flow**

```
                              COLLISION DETECTION
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ CREATE JEEP     │
                            │ BOUNDING BOX    │
                            │                 │
                            │ jeep_rect =     │
                            │ pygame.Rect()   │
                            └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ CHECK EACH      │
                            │ OBSTACLE        │
                            │                 │
                            │ for obstacle    │
                            │ in obstacles:   │
                            └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ COLLISION?      │
                            │                 │
                            │ jeep_rect.      │
                            │ colliderect()   │
                            └─────────────────┘
                                      │
                        ┌─────────────┼─────────────┐
                        │ NO          │             │ YES
                        ▼             │             ▼
                ┌─────────────┐       │   ┌─────────────────┐
                │ CONTINUE    │       │   │ Y-POSITION      │
                │ GAME LOOP   │       │   │ COMPARISON      │
                └─────────────┘       │   │                 │
                                      │   │ jeep.y <        │
                                      │   │ obstacle.y -    │
                                      │   │ height/4 ?      │
                                      │   └─────────────────┘
                                      │             │
                                      │   ┌─────────┼─────────┐
                                      │   │ YES     │         │ NO
                                      │   ▼         │         ▼
                                      │ ┌─────────────┐ ┌─────────────┐
                                      │ │ TOP HIT     │ │ SIDE HIT    │
                                      │ │             │ │             │
                                      │ │ fuel -= 0.2 │ │ health -= 8 │
                                      │ │ Small bounce│ │ Bounce back │
                                      │ │ Continue    │ │ Reset pos   │
                                      │ └─────────────┘ └─────────────┘
                                      │         │               │
                                      │         └───────────────┘
                                      │                 │
                                      └─────────────────┘
```

## ⛽ **Fuel Management System**

```
                              FUEL SYSTEM FLOW
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ FUEL CONSUMPTION│
                            │                 │
                            │ Moving: -0.04   │
                            │ Idle:   -0.01   │
                            │ Top Hit: -0.2   │
                            └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ FUEL CHECK      │
                            │                 │
                            │ if fuel <= 0:   │
                            └─────────────────┘
                                      │
                        ┌─────────────┼─────────────┐
                        │ FUEL > 0    │             │ FUEL = 0
                        ▼             │             ▼
                ┌─────────────┐       │   ┌─────────────────┐
                │ CONTINUE    │       │   │ SHOW REFUEL     │
                │ GAMEPLAY    │       │   │ MENU            │
                └─────────────┘       │   │                 │
                                      │   │ 5 Options:      │
                                      │   │ • +25% fuel     │
                                      │   │ • +50% fuel     │
                                      │   │ • +75% fuel     │
                                      │   │ • +100% fuel    │
                                      │   │ • Continue      │
                                      │   └─────────────────┘
                                      │             │
                                      │             ▼
                                      │   ┌─────────────────┐
                                      │   │ PLAYER SELECTS  │
                                      │   │ REFUEL OPTION   │
                                      │   │                 │
                                      │   │ fuel = min(100, │
                                      │   │ fuel + amount)  │
                                      │   └─────────────────┘
                                      │             │
                                      └─────────────┘
```

## 🏥 **Health System Flow**

```
                              HEALTH SYSTEM
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ HEALTH = 100    │
                          │ (Start Value)   │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ COLLISION TYPE  │
                          │ DETECTION       │
                          └─────────────────┘
                                    │
                      ┌─────────────┼─────────────┐
                      │ TOP HIT     │             │ SIDE HIT
                      ▼             │             ▼
              ┌─────────────┐       │     ┌─────────────┐
              │ NO HEALTH   │       │     │ HEALTH -= 8 │
              │ DAMAGE      │       │     │ (Damage)    │
              │             │       │     └─────────────┘
              │ Fuel cost   │       │             │
              │ instead     │       │             ▼
              └─────────────┘       │     ┌─────────────┐
                      │             │     │ HEALTH <= 0?│
                      │             │     └─────────────┘
                      │             │             │
                      │             │   ┌─────────┼─────────┐
                      │             │   │ NO      │         │ YES
                      │             │   ▼         │         ▼
                      │             │ ┌─────────────┐ ┌─────────────┐
                      │             │ │ CONTINUE    │ │ GAME OVER   │
                      │             │ │ PLAYING     │ │ SCREEN      │
                      │             │ └─────────────┘ └─────────────┘
                      │             │         │               │
                      └─────────────┼─────────┘               │
                                    │                         ▼
                                    │                 ┌─────────────┐
                                    │                 │ R: Restart  │
                                    │                 │ ESC: Menu   │
                                    │                 └─────────────┘
                                    │                         │
                                    └─────────────────────────┘
```

## 🎯 **Game State Transitions**

```
                              GAME STATE MACHINE
                                      │
                                      ▼
                            ┌─────────────────┐
                            │      MENU       │
                            │   (State = 0)   │
                            │                 │
                            │ • Navigation    │
                            │ • Option Select │
                            └─────────────────┘
                                      │
                        ┌─────────────┼─────────────┐
                        │ Start Game  │             │ Quit
                        ▼             │             ▼
                ┌─────────────┐       │     ┌─────────────┐
                │   PLAYING   │       │     │    EXIT     │
                │ (State = 1) │       │     │   GAME      │
                │             │       │     └─────────────┘
                │ • Physics   │       │
                │ • Collision │       │
                │ • Rendering │       │
                └─────────────┘       │
                        │             │
                        ▼             │
                ┌─────────────┐       │
                │ P Key Press │       │
                │ ESC Press   │       │
                └─────────────┘       │
                        │             │
                        ▼             │
                ┌─────────────┐       │
                │ PAUSE MENU  │       │
                │ (Back to    │       │
                │  Menu with  │       │
                │  Pause Mode)│       │
                └─────────────┘       │
                        │             │
                        └─────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ SPECIAL STATES  │
                            └─────────────────┘
                                      │
                        ┌─────────────┼─────────────┐
                        │ Fuel = 0    │             │ Health = 0
                        ▼             │             ▼
                ┌─────────────┐       │     ┌─────────────┐
                │ REFUEL MENU │       │     │ GAME OVER   │
                │ (State = 4) │       │     │ (State = 3) │
                │             │       │     │             │
                │ • 5 Options │       │     │ • Restart   │
                │ • Fuel Gauge│       │     │ • Menu      │
                └─────────────┘       │     └─────────────┘
                        │             │             │
                        └─────────────┼─────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ VICTORY CHECK   │
                            │                 │
                            │ jeep.x >=       │
                            │ finish_x ?      │
                            └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ WIN CONDITION   │
                            │                 │
                            │ • Victory Screen│
                            │ • Final Stats   │
                            │ • Play Again    │
                            └─────────────────┘
```

## 🌍 **World Generation Flow**

```
                              WORLD CREATION
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ TERRAIN         │
                          │ GENERATION      │
                          │                 │
                          │ • Hills/Valleys │
                          │ • 5000px wide   │
                          │ • Smooth curves │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ OBSTACLE        │
                          │ PLACEMENT       │
                          │                 │
                          │ • Rocks & Logs  │
                          │ • 160px spacing │
                          │ • 50% density   │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ ANIMAL          │
                          │ SPAWNING        │
                          │                 │
                          │ • 7 Types       │
                          │ • 200px spacing │
                          │ • 40% density   │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ BACKGROUND      │
                          │ ELEMENTS        │
                          │                 │
                          │ • Trees & Bushes│
                          │ • Static Pos    │
                          │ • No Random     │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ FINISH LINE     │
                          │ PLACEMENT       │
                          │                 │
                          │ • At x=4800     │
                          │ • Victory Goal  │
                          └─────────────────┘
```

## 🎨 **Rendering Order Flow**

```
                              FRAME RENDERING
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ CLEAR SCREEN    │
                          │ screen.fill()   │
                          │ (Black)         │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ LAYER 1:        │
                          │ TERRAIN         │
                          │                 │
                          │ • Sky gradient  │
                          │ • Ground fill   │
                          │ • Terrain poly  │
                          │ • Background    │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ LAYER 2:        │
                          │ ANIMALS         │
                          │                 │
                          │ • Background    │
                          │ • 7 Types       │
                          │ • Static poses  │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ LAYER 3:        │
                          │ OBSTACLES       │
                          │                 │
                          │ • Rocks         │
                          │ • Logs          │
                          │ • Textures      │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ LAYER 4:        │
                          │ FINISH LINE     │
                          │                 │
                          │ • Goal marker   │
                          │ • Victory flag  │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ LAYER 5:        │
                          │ JEEP (PLAYER)   │
                          │                 │
                          │ • Detailed      │
                          │ • Military      │
                          │ • Jump indicator│
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ LAYER 6:        │
                          │ HUD/UI          │
                          │                 │
                          │ • Health bar    │
                          │ • Fuel bar      │
                          │ • Speed/Distance│
                          │ • Instructions  │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ DISPLAY UPDATE  │
                          │ pygame.display. │
                          │ flip()          │
                          └─────────────────┘
```

---

**This comprehensive game mechanics flow chart illustrates every aspect of the Jungle Drive gameplay system, from player input to final rendering, showing the complete functional flow of the game.** 🎮🌴🚗
