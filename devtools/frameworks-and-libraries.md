# Frameworks & Libraries — PyTorch, Mineflayer, minecraft-protocol & go-mc

This reference covers key frameworks and libraries across two domains: deep learning with PyTorch for GPU-accelerated neural networks, and Minecraft automation with Mineflayer, minecraft-protocol, and go-mc for bot creation, protocol analysis, and server tooling. Despite their different domains, these libraries share a common theme of providing programmatic control over complex systems.

---

## Table of Contents
1. [PyTorch](#1-pytorch)
2. [Mineflayer](#2-mineflayer)
3. [minecraft-protocol](#3-minecraft-protocol)
4. [go-mc](#4-go-mc)
5. [Comparison Table](#5-comparison-table)

---

## 1. PyTorch

### Overview

PyTorch is Meta's open-source deep learning framework built for research flexibility and production deployment. It provides tensor computation with GPU acceleration and dynamic computation graphs (eager execution), making it the preferred framework in academia and increasingly in industry.

- **Website:** https://pytorch.org
- **Source:** https://github.com/pytorch/pytorch
- **License:** BSD-3-Clause
- **Language:** Python (with C++ backend)

### Installation

```bash
# CPU only
pip install torch torchvision torchaudio

# CUDA 12.1 (NVIDIA GPU support)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CUDA 12.4
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Conda (recommended for complex environments)
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

# Verify installation
python -c "import torch; print(torch.__version__); print('CUDA:', torch.cuda.is_available())"
```

### Core Concepts

#### Tensors

Tensors are the fundamental data structure in PyTorch — multi-dimensional arrays with GPU support.

```python
import torch

# Create tensors
x = torch.tensor([1.0, 2.0, 3.0])               # From list
y = torch.zeros(3, 4)                             # 3x4 matrix of zeros
z = torch.randn(3, 4)                             # 3x4 random normal
w = torch.ones(3, 4, device='cuda')               # On GPU

# Operations
a = x + y[0]                                      # Element-wise addition
b = torch.matmul(z, z.T)                          # Matrix multiplication
c = z.reshape(4, 3)                               # Reshape

# NumPy interop
import numpy as np
np_array = z.numpy()                               # Tensor → NumPy
tensor = torch.from_numpy(np_array)                # NumPy → Tensor
```

#### Autograd (Automatic Differentiation)

```python
# Autograd tracks operations for backpropagation
x = torch.tensor([2.0, 3.0], requires_grad=True)
y = x ** 2 + 3 * x
loss = y.sum()

loss.backward()        # Compute gradients
print(x.grad)          # dy/dx = 2x + 3 → tensor([7., 9.])
```

#### nn.Module (Building Neural Networks)

```python
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = SimpleNet()
print(model)
# Print parameter count
total_params = sum(p.numel() for p in model.parameters())
print(f"Parameters: {total_params:,}")
```

#### Training Loop

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Model, optimizer, loss function
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Dummy data (replace with real dataset)
X_train = torch.randn(1000, 784)
y_train = torch.randint(0, 10, (1000,))
dataset = TensorDataset(X_train, y_train)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

# Training loop
model.train()
for epoch in range(10):
    total_loss = 0
    for batch_X, batch_y in loader:
        optimizer.zero_grad()               # Clear gradients
        output = model(batch_X)             # Forward pass
        loss = criterion(output, batch_y)   # Compute loss
        loss.backward()                     # Backpropagation
        optimizer.step()                    # Update weights
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss/len(loader):.4f}")

# Save and load models
torch.save(model.state_dict(), 'model.pth')
model.load_state_dict(torch.load('model.pth'))
```

### Ecosystem

| Library | Purpose |
|---------|---------|
| **TorchVision** | Image datasets, models (ResNet, ViT), transforms |
| **TorchAudio** | Audio processing, speech models |
| **TorchText** | Text datasets and NLP utilities |
| **PyTorch Lightning** | High-level training framework (reduces boilerplate) |
| **Hugging Face Transformers** | Pre-trained LLMs and NLP models (built on PyTorch) |
| **ONNX** | Export PyTorch models for cross-platform inference |

### PyTorch vs TensorFlow

| Aspect | PyTorch | TensorFlow |
|--------|---------|------------|
| **Execution** | Eager (dynamic graphs) | Eager + Graph (tf.function) |
| **API Style** | Pythonic, intuitive | Keras high-level API |
| **Debugging** | Standard Python debugger | Requires tf.debugging tools |
| **Research adoption** | Dominant in academia | Still used, declining share |
| **Production** | TorchServe, ONNX | TF Serving, TF Lite, TF.js |
| **Mobile** | PyTorch Mobile (ExecuTorch) | TF Lite (mature) |
| **Community** | Fastest growing | Large, established |
| **Visualization** | TensorBoard (compatible) | TensorBoard (native) |

---

## 2. Mineflayer

### Overview

Mineflayer is a high-level Node.js library for creating Minecraft bots that can interact with the game world. It supports Minecraft Java Edition and provides APIs for movement, combat, crafting, inventory management, and more.

- **Website:** https://github.com/PrismarineJS/mineflayer
- **License:** MIT
- **Language:** JavaScript/Node.js
- **Minecraft Support:** Java Edition (multiple versions)

### Installation

```bash
# Initialize a Node.js project
mkdir my-bot && cd my-bot
npm init -y

# Install mineflayer
npm install mineflayer

# Common plugins
npm install mineflayer-pathfinder    # A* pathfinding
npm install mineflayer-pvp           # Combat automation
npm install mineflayer-armor-manager # Auto-equip best armor
npm install mineflayer-collectblock  # Collect/mine blocks
npm install prismarine-viewer        # 3D web viewer for debugging
```

### Basic Bot

```javascript
const mineflayer = require('mineflayer')

const bot = mineflayer.createBot({
  host: 'localhost',       // Minecraft server IP
  port: 25565,             // Server port
  username: 'Bot',         // Bot username
  // version: '1.20.4',    // Optional: specify Minecraft version
  // auth: 'microsoft',    // For online-mode servers
})

// Event: bot has spawned into the world
bot.on('spawn', () => {
  console.log('Bot spawned at', bot.entity.position)
  bot.chat('Hello, world!')
})

// Event: chat message received
bot.on('chat', (username, message) => {
  if (username === bot.username) return  // Ignore own messages

  if (message === 'hello') {
    bot.chat(`Hi, ${username}!`)
  }
  if (message === 'come') {
    const player = bot.players[username]?.entity
    if (player) {
      bot.lookAt(player.position.offset(0, 1.6, 0))
      bot.chat('On my way!')
    }
  }
})

// Event: bot was kicked
bot.on('kicked', (reason) => console.log('Kicked:', reason))

// Event: error
bot.on('error', (err) => console.log('Error:', err))
```

### Pathfinding

```javascript
const mineflayer = require('mineflayer')
const pathfinder = require('mineflayer-pathfinder')
const { GoalNear, GoalBlock, GoalFollow } = require('mineflayer-pathfinder').goals

const bot = mineflayer.createBot({ host: 'localhost', username: 'Bot' })

bot.loadPlugin(pathfinder.pathfinder)

bot.on('spawn', () => {
  const mcData = require('minecraft-data')(bot.version)
  const movements = new pathfinder.Movements(bot, mcData)
  movements.allowSprinting = true
  bot.pathfinder.setMovements(movements)
})

bot.on('chat', (username, message) => {
  if (message === 'follow me') {
    const player = bot.players[username]?.entity
    if (player) {
      bot.pathfinder.setGoal(new GoalFollow(player, 2), true)
      bot.chat('Following you!')
    }
  }
  if (message === 'stop') {
    bot.pathfinder.setGoal(null)
    bot.chat('Stopped.')
  }
})
```

### Block Interaction

```javascript
// Mine a block
bot.on('chat', async (username, message) => {
  if (message === 'dig') {
    const block = bot.blockAt(bot.entity.position.offset(0, -1, 0))
    if (block) {
      await bot.dig(block)
      bot.chat(`Dug ${block.name}`)
    }
  }
  if (message === 'place dirt') {
    const mcData = require('minecraft-data')(bot.version)
    const dirt = mcData.itemsByName.dirt.id
    const referenceBlock = bot.blockAt(bot.entity.position.offset(0, -1, 0))
    await bot.equip(dirt, 'hand')
    await bot.placeBlock(referenceBlock, { x: 0, y: 1, z: 0 })
  }
})
```

### Debugging with prismarine-viewer

```javascript
const { mineflayer: mineflayerViewer } = require('prismarine-viewer')

bot.on('spawn', () => {
  mineflayerViewer(bot, { port: 3000, firstPerson: false })
  console.log('Viewer running at http://localhost:3000')
})
```

Open `http://localhost:3000` in a browser to see a 3D view of the bot's world.

---

## 3. minecraft-protocol

### Overview

minecraft-protocol is a low-level Node.js library that implements the Minecraft network protocol. It handles packet serialization/deserialization, encryption, compression, and authentication, giving you full control over network communication.

- **Website:** https://github.com/PrismarineJS/node-minecraft-protocol
- **License:** MIT
- **Language:** JavaScript/Node.js
- **Use cases:** custom clients, proxies, protocol analysis, server status tools

### Installation

```bash
npm install minecraft-protocol
```

### Server Status Ping

```javascript
const mc = require('minecraft-protocol')

// Ping a server for status (no login required)
mc.ping({ host: 'localhost', port: 25565 }, (err, result) => {
  if (err) return console.error(err)
  console.log('Server:', result.description)
  console.log('Players:', `${result.players.online}/${result.players.max}`)
  console.log('Version:', result.version.name)
  console.log('Latency:', result.latency, 'ms')
})
```

### Custom Client

```javascript
const mc = require('minecraft-protocol')

const client = mc.createClient({
  host: 'localhost',
  port: 25565,
  username: 'ProtocolBot',
  // auth: 'microsoft',   // For online-mode servers
})

// Listen for all packets (protocol analysis)
client.on('packet', (data, meta) => {
  console.log(`[${meta.state}] ${meta.name}`, JSON.stringify(data).slice(0, 100))
})

// Listen for specific packet types
client.on('chat', (packet) => {
  console.log('Chat:', JSON.parse(packet.message))
})

// Send a chat message
client.on('login', () => {
  setTimeout(() => {
    client.write('chat', { message: 'Hello from protocol!' })
  }, 3000)
})
```

### Simple Proxy

```javascript
const mc = require('minecraft-protocol')

// Create a server that forwards traffic to a real server
const server = mc.createServer({
  'online-mode': false,
  port: 25566,
  version: '1.20.4',
})

server.on('login', (client) => {
  const target = mc.createClient({
    host: 'localhost',
    port: 25565,
    username: client.username,
  })

  // Forward packets in both directions
  client.on('packet', (data, meta) => {
    if (target.state === meta.state && meta.name !== 'keep_alive') {
      target.write(meta.name, data)
    }
  })

  target.on('packet', (data, meta) => {
    if (client.state === meta.state && meta.name !== 'keep_alive') {
      client.write(meta.name, data)
    }
  })
})
```

### Mineflayer vs minecraft-protocol

| Aspect | Mineflayer | minecraft-protocol |
|--------|------------|--------------------|
| **Level** | High-level (game logic) | Low-level (packets) |
| **API** | `bot.chat()`, `bot.dig()`, `bot.pathfinder` | `client.write('chat', {...})` |
| **World awareness** | Yes (blocks, entities, inventory) | No (raw packets only) |
| **Use case** | Bots, automation | Proxies, protocol tools, custom clients |
| **Built on** | minecraft-protocol | N/A (standalone) |

---

## 4. go-mc

### Overview

go-mc is a Go library for interacting with Minecraft servers and protocols. It provides client-side bot creation, server status pinging, RCON (remote console), and low-level protocol handling in Go.

- **Website:** https://github.com/Tnze/go-mc
- **License:** MIT
- **Language:** Go

### Installation

```bash
# Add to your Go project
go get github.com/Tnze/go-mc@latest
```

### Server Status Ping

```go
package main

import (
    "fmt"
    "github.com/Tnze/go-mc/bot"
    "github.com/Tnze/go-mc/bot/basic"
)

func main() {
    resp, delay, err := bot.PingAndList("localhost:25565")
    if err != nil {
        panic(err)
    }
    fmt.Printf("Server response: %s\n", resp)
    fmt.Printf("Latency: %dms\n", delay.Milliseconds())
}
```

### Basic Bot

```go
package main

import (
    "fmt"
    "github.com/Tnze/go-mc/bot"
    "github.com/Tnze/go-mc/bot/basic"
    "github.com/Tnze/go-mc/chat"
)

func main() {
    client := bot.NewClient()
    client.Auth = bot.Auth{
        Name: "GoBot",
    }

    // Set up basic player handler
    player := basic.NewPlayer(client, basic.Settings{
        Locale:   "en_US",
        ViewDist: 8,
    })

    // Handle chat messages
    basic.EventsListener{
        GameStart: func() error {
            fmt.Println("Bot joined the game")
            return player.Chat("Hello from Go!")
        },
        ChatMsg: func(msg chat.Message, _ bool) error {
            fmt.Printf("Chat: %s\n", msg)
            return nil
        },
        Disconnect: func(reason chat.Message) error {
            fmt.Printf("Disconnected: %s\n", reason)
            return nil
        },
    }.Attach(client)

    // Connect to server
    err := client.JoinServer("localhost:25565")
    if err != nil {
        panic(err)
    }

    // Handle events
    for {
        if err := client.HandleGame(); err != nil {
            fmt.Printf("Error: %v\n", err)
            break
        }
    }
}
```

### RCON (Remote Console)

```go
package main

import (
    "fmt"
    "github.com/Tnze/go-mc/net"
)

func main() {
    // Connect to Minecraft RCON
    conn, err := net.DialRCON("localhost:25575", "rcon-password")
    if err != nil {
        panic(err)
    }
    defer conn.Close()

    // Send a command
    resp, err := conn.Cmd("list")
    if err != nil {
        panic(err)
    }
    fmt.Printf("Online players: %s\n", resp)

    // More commands
    resp, err = conn.Cmd("say Hello from RCON!")
    if err != nil {
        panic(err)
    }
}
```

### Why Go for Minecraft?

- **Performance** — compiled binary, low memory footprint, excellent concurrency
- **Single binary** — deploy a bot or tool as one executable with no runtime dependencies
- **Concurrency** — goroutines make it easy to handle multiple connections or tasks
- **Cross-compilation** — build for any platform from any platform (`GOOS=linux GOARCH=arm64 go build`)

---

## 5. Comparison Table

| Feature | PyTorch | Mineflayer | minecraft-protocol | go-mc |
|---------|---------|------------|--------------------|-------|
| **Language** | Python | JavaScript (Node.js) | JavaScript (Node.js) | Go |
| **Domain** | Deep learning | Minecraft bots | Minecraft protocol | Minecraft protocol |
| **Level** | High-level framework | High-level (game API) | Low-level (packets) | Mid-level |
| **Bot Support** | N/A | Yes (primary purpose) | Manual (packet-level) | Yes |
| **Server Support** | N/A | No | Yes (create servers) | Partial |
| **GPU Support** | Yes (CUDA, ROCm, MPS) | N/A | N/A | N/A |
| **Ecosystem** | TorchVision, Lightning, HF | pathfinder, pvp, viewer | Part of PrismarineJS | Standalone |
| **Active Development** | Yes (Meta + community) | Yes (PrismarineJS) | Yes (PrismarineJS) | Yes |
| **Use Case** | Neural networks, AI research | Game automation, AI agents | Proxies, protocol tools | Bots, server tools, RCON |
| **Install** | `pip install torch` | `npm install mineflayer` | `npm install minecraft-protocol` | `go get github.com/Tnze/go-mc` |
| **License** | BSD-3-Clause | MIT | MIT | MIT |

---

## See Also

- [Docker Essentials](docker-essentials.md) — Containerize PyTorch training environments and Minecraft servers
- [Editors & IDEs](editors-and-ides.md) — Set up VS Code for Python/Node.js/Go development
- [Terminal Tools](terminal-tools.md) — Use tmux for persistent bot sessions
- [APIs & Resources](../reference/apis-and-resources.md) — API keys and cloud GPU providers
