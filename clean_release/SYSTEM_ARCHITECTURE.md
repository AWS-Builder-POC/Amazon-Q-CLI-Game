# 🏗️ Jungle Drive - System Architecture Diagram

## 🔧 **High-Level System Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           JUNGLE DRIVE GAME SYSTEM                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   INPUT LAYER   │    │  GAME LOGIC     │    │  RENDER LAYER   │             │
│  │                 │    │     LAYER       │    │                 │             │
│  │  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │             │
│  │  │ Keyboard  │  │◄──►│  │   Game    │  │◄──►│  │  Screen   │  │             │
│  │  │   Events  │  │    │  │Controller │  │    │  │ Rendering │  │             │
│  │  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │             │
│  │  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │             │
│  │  │   Menu    │  │    │  │   State   │  │    │  │  Graphics │  │             │
│  │  │Navigation │  │    │  │ Manager   │  │    │  │ Pipeline  │  │             │
│  │  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│           │                       │                       │                     │
│           ▼                       ▼                       ▼                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        PYGAME FRAMEWORK                                 │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │   │
│  │  │   Events    │  │   Display   │  │   Surface   │  │    Clock    │    │   │
│  │  │   System    │  │   Manager   │  │   Drawing   │  │   Control   │    │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                     │                                           │
│                                     ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         PYTHON RUNTIME                                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🎮 **Game Component Architecture**

```
                              ┌─────────────────────────────────┐
                              │         GAME CLASS              │
                              │      (Main Controller)          │
                              │                                 │
                              │  • State Management             │
                              │  • Main Game Loop               │
                              │  • Input Coordination           │
                              │  • Rendering Coordination       │
                              └─────────────┬───────────────────┘
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
                    ▼                       ▼                       ▼
        ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
        │    MENU SYSTEM      │ │   GAME ENTITIES     │ │   WORLD SYSTEM      │
        │                     │ │                     │ │                     │
        │ ┌─────────────────┐ │ │ ┌─────────────────┐ │ │ ┌─────────────────┐ │
        │ │      Menu       │ │ │ │      Jeep       │ │ │ │    Terrain      │ │
        │ │   Navigation    │ │ │ │   (Player)      │ │ │ │   Generator     │ │
        │ └─────────────────┘ │ │ └─────────────────┘ │ │ └─────────────────┘ │
        │ ┌─────────────────┐ │ │ ┌─────────────────┐ │ │ ┌─────────────────┐ │
        │ │   Refuel Menu   │ │ │ │    Animals      │ │ │ │   Obstacles     │ │
        │ │   (5 Options)   │ │ │ │   (7 Types)     │ │ │ │ (Rocks & Logs)  │ │
        │ └─────────────────┘ │ │ └─────────────────┘ │ │ └─────────────────┘ │
        │ ┌─────────────────┐ │ │ ┌─────────────────┐ │ │ ┌─────────────────┐ │
        │ │  Pause System   │ │ │ │   Collision     │ │ │ │     Camera      │ │
        │ │ (State Change)  │ │ │ │    System       │ │ │ │   Following     │ │
        │ └─────────────────┘ │ │ └─────────────────┘ │ │ └─────────────────┘ │
        └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
                    │                       │                       │
                    └───────────────────────┼───────────────────────┘
                                            │
                                            ▼
                              ┌─────────────────────────────────┐
                              │      RENDERING PIPELINE         │
                              │                                 │
                              │  1. Clear Screen                │
                              │  2. Draw Terrain                │
                              │  3. Draw Animals (Background)   │
                              │  4. Draw Obstacles              │
                              │  5. Draw Jeep (Player)          │
                              │  6. Draw HUD/UI                 │
                              │  7. Display Update              │
                              └─────────────────────────────────┘
```

## 🔄 **Data Flow Architecture**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW DIAGRAM                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

INPUT EVENTS                    GAME STATE                     RENDER OUTPUT
     │                              │                              │
     ▼                              ▼                              ▼
┌─────────┐                   ┌─────────────┐                ┌─────────┐
│Keyboard │ ──────────────────►│    Game     │──────────────► │ Screen  │
│ Events  │                   │ Controller  │                │Display  │
└─────────┘                   └─────────────┘                └─────────┘
     │                              │                              │
     │         ┌─────────────────────┼─────────────────────┐        │
     │         │                     │                     │        │
     ▼         ▼                     ▼                     ▼        ▼
┌─────────┐ ┌─────────┐        ┌─────────┐        ┌─────────┐ ┌─────────┐
│  Menu   │ │  Jeep   │        │  World  │        │Animals  │ │   HUD   │
│ Input   │ │ Input   │        │  State  │        │ State   │ │Elements │
└─────────┘ └─────────┘        └─────────┘        └─────────┘ └─────────┘
     │         │                     │                     │        │
     │         │        ┌────────────┼────────────┐        │        │
     │         │        │            │            │        │        │
     ▼         ▼        ▼            ▼            ▼        ▼        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        GAME STATE UPDATES                              │
│                                                                         │
│  Menu Selection ──► State Transitions ──► Entity Updates ──► Rendering │
│       │                    │                    │                │     │
│       ▼                    ▼                    ▼                ▼     │
│  Navigation         MENU ◄──► PLAYING      Physics Update    Graphics  │
│  Validation         PAUSE ◄──► REFUEL      Collision Check   Pipeline  │
│  State Change       GAME_OVER              Resource Mgmt     UI Update  │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🧩 **Class Relationship Diagram**

```
                                    Game
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
                  Menu         RefuelMenu        GameWorld
                    │                │                │
            ┌───────┼───────┐        │        ┌───────┼───────┐
            │       │       │        │        │       │       │
            ▼       ▼       ▼        ▼        ▼       ▼       ▼
        Options  Input   Draw    FuelOptions Jeep  Animals Obstacles
                 │       │                    │       │       │
                 │       │                    │   ┌───┼───┐   │
                 │       │                    │   │   │   │   │
                 ▼       ▼                    ▼   ▼   ▼   ▼   ▼
            KeyDetect Rendering           Physics │   │   │  Rocks
                                                  │   │   │   │
                                                  ▼   ▼   ▼   ▼
                                            Elephant│   │  Logs
                                                Tiger│   │
                                                 Bear│   │
                                                 Deer▼   ▼
                                              Squirrel Bird
                                                Monkey
```

## ⚙️ **System Components Detail**

### **1. Input System Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PROCESSING                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  pygame.event.get() ──► Event Queue ──► Event Handler      │
│           │                   │               │             │
│           ▼                   ▼               ▼             │
│    ┌─────────────┐    ┌─────────────┐  ┌─────────────┐     │
│    │   KEYDOWN   │    │   KEYUP     │  │    QUIT     │     │
│    │   Events    │    │   Events    │  │   Events    │     │
│    └─────────────┘    └─────────────┘  └─────────────┘     │
│           │                   │               │             │
│           ▼                   ▼               ▼             │
│    ┌─────────────────────────────────────────────────────┐ │
│    │           KEY STATE DETECTION                       │ │
│    │                                                     │ │
│    │  keys_pressed = pygame.key.get_pressed()           │ │
│    │  keys_just_pressed = current - last_frame          │ │
│    │  keys_pressed_last_frame = current_keys            │ │
│    └─────────────────────────────────────────────────────┘ │
│                           │                                 │
│                           ▼                                 │
│    ┌─────────────────────────────────────────────────────┐ │
│    │              INPUT ROUTING                          │ │
│    │                                                     │ │
│    │  if state == MENU: ──► Menu.handle_input()         │ │
│    │  if state == PLAYING: ──► Jeep.update()            │ │
│    │  if state == REFUEL: ──► RefuelMenu.handle_input() │ │
│    └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **2. Physics System Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                   PHYSICS PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input Forces ──► Velocity Update ──► Position Update      │
│       │                  │                    │             │
│       ▼                  ▼                    ▼             │
│  ┌─────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │Keyboard │      │  Physics    │      │  Position   │     │
│  │ Input   │ ──►  │ Calculation │ ──►  │   Update    │     │
│  └─────────┘      └─────────────┘      └─────────────┘     │
│       │                  │                    │             │
│       │                  ▼                    ▼             │
│       │           ┌─────────────┐      ┌─────────────┐     │
│       │           │   Gravity   │      │  Collision  │     │
│       └──────────►│  Friction   │ ──►  │  Detection  │     │
│                   │   Forces    │      │   & Response│     │
│                   └─────────────┘      └─────────────┘     │
│                          │                    │             │
│                          ▼                    ▼             │
│                   ┌─────────────┐      ┌─────────────┐     │
│                   │  Boundary   │      │   Terrain   │     │
│                   │   Checks    │      │  Collision  │     │
│                   └─────────────┘      └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### **3. Collision System Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                 COLLISION DETECTION                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Jeep Bounding Box ──► Collision Check ──► Response        │
│         │                     │                 │           │
│         ▼                     ▼                 ▼           │
│  ┌─────────────┐      ┌─────────────┐    ┌─────────────┐   │
│  │   Jeep      │      │  Obstacle   │    │  Collision  │   │
│  │ Rectangle   │ ──►  │   Check     │──► │  Response   │   │
│  └─────────────┘      └─────────────┘    └─────────────┘   │
│         │                     │                 │           │
│         │                     ▼                 ▼           │
│         │              ┌─────────────┐    ┌─────────────┐   │
│         │              │Y-Position   │    │ Top Hit:    │   │
│         └─────────────►│ Comparison  │──► │ Fuel -= 0.2 │   │
│                        └─────────────┘    └─────────────┘   │
│                               │                 │           │
│                               ▼                 ▼           │
│                        ┌─────────────┐    ┌─────────────┐   │
│                        │   Smart     │    │ Side Hit:   │   │
│                        │ Detection   │──► │Health -= 8  │   │
│                        └─────────────┘    │Bounce Back  │   │
│                                           └─────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### **4. Rendering System Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                  RENDERING PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frame Start ──► Clear Screen ──► Layer Rendering ──► End  │
│       │               │                  │             │   │
│       ▼               ▼                  ▼             ▼   │
│  ┌─────────┐   ┌─────────────┐   ┌─────────────┐  ┌──────┐ │
│  │ 60 FPS  │   │screen.fill  │   │   Layer     │  │Flip  │ │
│  │ Timer   │──►│  (black)    │──►│  Rendering  │─►│Screen│ │
│  └─────────┘   └─────────────┘   └─────────────┘  └──────┘ │
│                                         │                   │
│                                         ▼                   │
│                                  ┌─────────────┐           │
│                                  │   Layers:   │           │
│                                  │             │           │
│                                  │ 1.Terrain  │           │
│                                  │ 2.Animals  │           │
│                                  │ 3.Obstacles│           │
│                                  │ 4.Jeep     │           │
│                                  │ 5.HUD/UI   │           │
│                                  └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 **Performance Architecture**

### **Memory Management**
```
┌─────────────────────────────────────────────────────────────┐
│                   MEMORY ALLOCATION                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Static Assets ──► Dynamic Objects ──► Garbage Collection  │
│       │                  │                    │             │
│       ▼                  ▼                    ▼             │
│  ┌─────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │ Sprites │      │   Game      │      │   Python    │     │
│  │ Colors  │      │  Objects    │      │     GC      │     │
│  │Constants│      │  (Dynamic)  │      │ (Automatic) │     │
│  └─────────┘      └─────────────┘      └─────────────┘     │
│       │                  │                    │             │
│       │                  ▼                    │             │
│       │           ┌─────────────┐             │             │
│       │           │   Object    │             │             │
│       └──────────►│    Pool     │◄────────────┘             │
│                   │ Management  │                           │
│                   └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

### **Performance Optimization**
```
┌─────────────────────────────────────────────────────────────┐
│                 PERFORMANCE STRATEGIES                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  • 60 FPS Target with pygame.Clock                         │
│  • Efficient Collision Detection (Bounding Boxes)          │
│  • Static Background Generation (No Random in Draw)        │
│  • Minimal Animal Movement (1/1000 chance)                 │
│  • Camera Culling (Only draw visible objects)              │
│  • Memory-Efficient Sprite Rendering                       │
│  • Single-Pass Terrain Generation                          │
│  • Optimized Input Detection (Key State Caching)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**This comprehensive system architecture diagram shows the complete technical structure of the Jungle Drive game, from high-level components down to detailed subsystem interactions.** 🏗️🎮🌴
