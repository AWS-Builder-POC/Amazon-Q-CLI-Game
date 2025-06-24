# 🎮 Jungle Drive - Complete Functional Flow Diagram

## 🔄 Game State Flow Chart

```
                    ┌─────────────────────────────────────────────────────────┐
                    │                   GAME START                            │
                    │                pygame.init()                            │
                    │              Initialize Constants                       │
                    └─────────────────────┬───────────────────────────────────┘
                                          │
                                          ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │                  MAIN MENU                              │
                    │  ┌─────────────────────────────────────────────────┐    │
                    │  │  🎯 Start the Drive                             │    │
                    │  │  🛑 Rest on Tyres                               │    │
                    │  │  🚪 Park Out of Jungle                          │    │
                    │  └─────────────────────────────────────────────────┘    │
                    │           ↑↓ Arrow Keys | ENTER Select                  │
                    └─────┬─────────────┬─────────────┬─────────────────────────┘
                          │             │             │
                    ┌─────▼─────┐  ┌────▼────┐  ┌────▼────┐
                    │START GAME │  │ RESUME  │  │  QUIT   │
                    │(Option 0) │  │(Option 1)│  │(Option 2)│
                    └─────┬─────┘  └────┬────┘  └────┬────┘
                          │             │             │
                          ▼             │             ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │                 GAME PLAYING                            │
                    │  ┌─────────────────────────────────────────────────┐    │
                    │  │  🚗 Jeep Physics & Movement                     │    │
                    │  │  🌍 Terrain Generation & Scrolling              │    │
                    │  │  🐘 Animal Updates (7 types)                    │    │
                    │  │  🪨 Obstacle Collision Detection                │    │
                    │  │  ⛽ Fuel & Health Management                    │    │
                    │  │  📊 HUD Display                                 │    │
                    │  └─────────────────────────────────────────────────┘    │
                    │     →← Accelerate/Brake | ↑ Jump | ↓ Fast Drop          │
                    │     P Pause | ESC Menu                                  │
                    └─────┬─────────────┬─────────────┬─────────────────────────┘
                          │             │             │
                    ┌─────▼─────┐  ┌────▼────┐  ┌────▼────┐
                    │   PAUSE   │  │FUEL=0   │  │HEALTH=0 │
                    │  (P Key)  │  │REFUEL   │  │GAME OVER│
                    └─────┬─────┘  └────┬────┘  └────┬────┘
                          │             │             │
                          ▼             ▼             ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │                PAUSE MENU                               │
                    │  ┌─────────────────────────────────────────────────┐    │
                    │  │  🔄 Start the Engine Again                      │    │
                    │  │  😴 Resting on Tyres (grayed out)              │    │
                    │  │  🚪 Park Out of Jungle                          │    │
                    │  └─────────────────────────────────────────────────┘    │
                    └─────────────────────┬───────────────────────────────────┘
                                          │
                                          ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │                REFUEL MENU                              │
                    │  ┌─────────────────────────────────────────────────┐    │
                    │  │  ⛽ Emergency Fuel (+25%)                       │    │
                    │  │  ⛽ Standard Refuel (+50%)                      │    │
                    │  │  ⛽ Premium Fill (+75%)                         │    │
                    │  │  ⛽ Full Tank (+100%)                           │    │
                    │  │  ➡️ Continue with Current Fuel                  │    │
                    │  └─────────────────────────────────────────────────┘    │
                    │           Visual Fuel Gauge Display                     │
                    └─────────────────────┬───────────────────────────────────┘
                                          │
                                          ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │                GAME OVER                                │
                    │  ┌─────────────────────────────────────────────────┐    │
                    │  │  💀 Health Depleted OR 🏁 Victory Achieved      │    │
                    │  │  📊 Final Stats Display                         │    │
                    │  │  R Restart | ESC Menu                          │    │
                    │  └─────────────────────────────────────────────────┘    │
                    └─────────────────────┬───────────────────────────────────┘
                                          │
                                          ▼
                                    [BACK TO MENU]
```

## 🎯 Detailed Component Flow

### 1. 🎮 **Game Initialization Flow**
```
Game.__init__()
├── pygame.init()
├── Screen Setup (1200x800)
├── Clock Setup (60 FPS)
├── State = MENU
├── Menu.__init__()
├── RefuelMenu.__init__()
└── keys_pressed_last_frame = set()
```

### 2. 🎯 **Menu System Flow**
```
Menu State (MENU = 0)
├── Menu.update()
│   └── title_animation += 0.02
├── Menu.handle_input(keys_just_pressed)
│   ├── UP Arrow → selected_option -= 1
│   ├── DOWN Arrow → selected_option += 1
│   └── ENTER → return selected_option
├── Menu.draw(screen)
│   ├── Retro sunset background
│   ├── Large detailed jeep
│   ├── Animal silhouettes
│   ├── Menu options with highlighting
│   └── Instructions
└── Option Selection:
    ├── 0: Start/Resume Game
    ├── 1: Pause (if game exists)
    └── 2: Quit Game
```

### 3. 🚗 **Gameplay Flow**
```
Playing State (PLAYING = 1)
├── Input Handling
│   ├── → Right: velocity_x += acceleration
│   ├── ← Left: velocity_x -= acceleration
│   ├── ↑ Up: Jump (if on_ground)
│   ├── ↓ Down: Fast descent
│   ├── P: Pause → MENU state
│   └── ESC: Return to menu
├── Jeep.update()
│   ├── Apply physics (gravity, friction)
│   ├── Update position
│   ├── Terrain collision detection
│   ├── Obstacle collision (smart system)
│   │   ├── Top collision: fuel -= 0.2
│   │   └── Side collision: health -= 8
│   └── Fuel consumption
├── Camera.update()
│   └── camera_x = jeep.x - SCREEN_WIDTH/3
├── Animal.update() (for each animal)
│   └── Minimal movement (1 in 1000 chance)
├── Win/Lose Condition Check
│   ├── jeep.x >= finish_x → Victory
│   ├── jeep.health <= 0 → Game Over
│   └── jeep.fuel <= 0 → Refuel Menu
└── Rendering Pipeline
    ├── Clear screen (black)
    ├── Draw terrain (sky + ground)
    ├── Draw animals (background)
    ├── Draw obstacles (rocks/logs)
    ├── Draw finish line
    ├── Draw jeep
    └── Draw HUD
```

### 4. ⛽ **Refuel System Flow**
```
Refuel State (REFUEL_MENU = 4)
├── Triggered when: jeep.fuel <= 0
├── RefuelMenu.update()
│   └── title_animation += 0.03
├── RefuelMenu.handle_input()
│   ├── UP/DOWN: Navigate options
│   └── ENTER: Select refuel amount
├── RefuelMenu.draw()
│   ├── Semi-transparent overlay
│   ├── Fuel gauge visualization
│   ├── 5 refuel options
│   └── Current fuel display
└── Refuel Options:
    ├── 0: +25% fuel
    ├── 1: +50% fuel
    ├── 2: +75% fuel
    ├── 3: +100% fuel
    └── 4: Continue without refuel
```

### 5. ⏸️ **Pause System Flow**
```
Pause Trigger (P Key pressed)
├── Set menu.is_paused = True
├── Update menu options:
│   ├── Option 0: "Start the Engine Again"
│   ├── Option 1: "Resting on Tyres" (grayed)
│   └── Option 2: "Park Out of Jungle"
├── State = MENU
└── Resume Options:
    ├── Select Option 0 → Resume game
    └── Select Option 2 → Quit game
```

## 🔧 **Technical Component Interaction**

### **Class Interaction Diagram**
```
Game (Main Controller)
├── Menu
│   ├── handle_input() → Game.handle_input()
│   ├── update() → Animation updates
│   └── draw() → Render menu elements
├── RefuelMenu
│   ├── handle_input() → Fuel selection
│   ├── update() → Animation updates
│   └── draw() → Render refuel interface
├── Jeep (Player)
│   ├── update() → Physics, collision, fuel
│   └── draw() → Detailed military jeep
├── Animal[] (Wildlife)
│   ├── update() → Minimal movement
│   └── draw() → 7 different animal types
├── Obstacle[] (Terrain)
│   ├── Static objects (rocks, logs)
│   └── draw() → Render obstacles
└── World Generation
    ├── generate_terrain() → Hills and valleys
    ├── generate_obstacles() → Rock/log placement
    └── generate_animals() → Wildlife spawning
```

### **Collision Detection Flow**
```
Jeep-Obstacle Collision
├── Create jeep_rect (bounding box)
├── For each obstacle:
│   ├── Check collision with obstacle.rect
│   ├── If collision detected:
│   │   ├── Check Y-position comparison
│   │   ├── If jeep.y < obstacle.y - height/4:
│   │   │   ├── TOP COLLISION
│   │   │   ├── fuel -= 0.2 (2x consumption)
│   │   │   └── Small bounce effect
│   │   └── Else:
│   │       ├── SIDE COLLISION
│   │       ├── Reset position (bounce back)
│   │       ├── velocity_x *= -0.3
│   │       └── health -= 8
│   └── Break (handle one collision per frame)
└── Continue game loop
```

### **State Management Flow**
```
Game States (Finite State Machine)
├── MENU (0)
│   ├── Show main menu
│   ├── Handle menu navigation
│   └── Transition to PLAYING or quit
├── PLAYING (1)
│   ├── Active gameplay
│   ├── Physics updates
│   ├── Collision detection
│   └── Transition to MENU, REFUEL_MENU, or GAME_OVER
├── PAUSED (2) [Unused - uses MENU instead]
├── GAME_OVER (3)
│   ├── Show end screen
│   ├── Display final stats
│   └── Options: Restart or Menu
└── REFUEL_MENU (4)
    ├── Show fuel options
    ├── Handle refuel selection
    └── Return to PLAYING
```

## 🎨 **Rendering Pipeline**

### **Frame Rendering Order**
```
Each Frame (60 FPS):
1. Handle Events (pygame.event.get())
2. Handle Input (key detection)
3. Update Game State
   ├── Menu updates (if MENU state)
   ├── Jeep physics (if PLAYING state)
   ├── Animal updates (if PLAYING state)
   └── Camera updates (if PLAYING state)
4. Clear Screen (screen.fill(black))
5. Render Based on State:
   ├── MENU: Menu.draw()
   ├── PLAYING: Game world rendering
   ├── REFUEL_MENU: Game world + refuel overlay
   └── GAME_OVER: End screen
6. Display Update (pygame.display.flip())
7. Clock Tick (60 FPS limit)
```

### **Game World Rendering Order**
```
Game World Rendering (PLAYING state):
1. Draw Terrain
   ├── Sky gradient (top half)
   ├── Ground base fill
   ├── Terrain polygon
   └── Background elements (trees, bushes)
2. Draw Animals (Background layer)
   ├── 7 animal types
   └── Static poses (no rotation)
3. Draw Obstacles (Mid layer)
   ├── Rocks with texture
   └── Logs with wood grain
4. Draw Finish Line (Goal)
5. Draw Jeep (Player layer)
   ├── Detailed military vehicle
   └── Jump indicator (if airborne)
6. Draw HUD (UI layer)
   ├── Health bar (red)
   ├── Fuel bar (blue)
   ├── Speed and distance
   ├── Pause instruction
   └── Control instructions
```

---

**This comprehensive flow diagram shows every aspect of the Jungle Drive game's functional architecture, from initialization to gameplay mechanics to state transitions.** 🌴🚗🎮
