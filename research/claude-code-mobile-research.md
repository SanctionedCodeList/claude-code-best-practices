# Claude Code Mobile Access Research

*Research date: 2026-01-07*

## Summary

This research documents best practices and tools for running Claude Code from mobile devices, based on blog posts, Hacker News discussions, and power user workflows.

## The Power User Standard: SSH + tmux + Tailscale

The most recommended approach across all sources combines:

1. **Tailscale** - P2P VPN between phone and desktop (no port forwarding needed)
2. **tmux** - Terminal multiplexer keeps sessions alive across disconnects
3. **SSH client** - Termius, Blink Shell (iOS), or Termux (Android)
4. **Mosh** (optional) - Mobile shell, better than SSH for unstable connections

### Why This Approach Wins

- Full terminal control identical to desktop
- Sessions survive disconnects, phone reboots, network changes
- No third-party servers seeing code
- Works with existing Claude Code setup
- Free (no subscription beyond Claude Pro)

### Setup Steps

1. Enable SSH on workstation (macOS: Settings → General → Sharing → Remote Login)
2. Install Tailscale on both devices, log in with same account
3. Install tmux on workstation
4. Install SSH client on phone (Blink Shell recommended for iOS)
5. Connect via Tailscale hostname: `ssh user@machine-name`
6. Start tmux session: `tmux new -s claude`
7. Run Claude Code inside tmux

### Enhanced Setup Options

**Push notifications** (via ntfy app):
- Alert when Claude waits 60+ seconds for input
- Free, self-hostable

**Mosh for unstable connections**:
- Survives network changes without dropping
- Better for cellular roaming
- Install: `brew install mosh` (macOS)

**Custom terminal layouts**:
- Zellij or tmux layouts optimized for mobile screens
- Separate panes for Claude Code, monitoring, git

## Understanding Tailscale

### What is Tailscale?

Tailscale is a mesh VPN that creates a private network (called a "tailnet") between your devices. Unlike traditional VPNs that route everything through a central server, Tailscale connects devices **directly to each other** (peer-to-peer).

### How it works

1. **Built on WireGuard** - Uses the fast, modern WireGuard encryption protocol
2. **NAT traversal** - Automatically punches through firewalls without port forwarding
3. **Peer-to-peer** - Traffic flows directly between devices, not through Tailscale's servers
4. **Control plane only** - Tailscale servers just exchange encryption keys and policies; your actual data never touches them

### Why it's ideal for Claude Code mobile access

- Install on phone + desktop → instantly on the same private network
- No firewall configuration, no dynamic DNS, no port forwarding
- Works across home WiFi, cellular, coffee shop networks
- Free tier covers personal use (up to 100 devices)
- Private keys never leave the device

### Self-Hosted Alternatives

For users who want full control over their infrastructure:

| Tool | Description | Best For |
|------|-------------|----------|
| **[Headscale](https://github.com/juanfont/headscale)** | Open source Tailscale control server replacement | Existing Tailscale users; uses official clients |
| **[NetBird](https://netbird.io/)** | Full open source mesh VPN with own clients + web UI | Complete self-hosted solution; easiest setup |
| **[ZeroTier](https://zerotier.com/)** | SD-WAN + VPN hybrid, custom protocol | Multicast/IoT support, VLAN-style networking |
| **[Nebula](https://github.com/slackhq/nebula)** | Slack's mesh networking tool | High performance, proven at scale |
| **[Netmaker](https://netmaker.io/)** | WireGuard mesh with enterprise features | Site-to-site, load balancing |

### Comparison

| | Tailscale | Headscale | NetBird | ZeroTier |
|--|-----------|-----------|---------|----------|
| **Self-hosted** | No (control plane) | Yes | Yes | Partial |
| **Protocol** | WireGuard | WireGuard | WireGuard | Custom |
| **Setup difficulty** | Easiest | Medium | Easy | Medium |
| **Cost** | Free tier, then paid | Free | Free | Free tier, then paid |
| **Vendor lock-in** | Some | None | None | Some |

### Recommendation

- **Just want it to work**: Tailscale free tier
- **Want full control, easy setup**: NetBird - "measurably quicker to setup than every other self-hosted tool"
- **Already use Tailscale clients**: Headscale - drop-in replacement for control server

## Third-Party Tools

### Happy Coder
- **URL**: https://happy.engineering/
- **Install**: `npm i -g happy-coder`
- **Features**: E2E encrypted, voice input, push notifications, multiple sessions
- **Platforms**: iOS, Android, web
- **Source**: Open source, MIT licensed

### Clauder
- **URL**: https://github.com/ZohaibAhmed/clauder
- **Features**: iPhone app with passcode auth, real-time sync
- **Setup**: `clauder quickstart` launches everything
- **Security**: 256-bit tokens, 24-hour expiration

### Omnara
- **URL**: https://omnara.dev (from HN)
- **Install**: `pip install omnara && omnara`
- **Features**: Web dashboard, mobile app, session continuity
- **Note**: Messages stored on their servers (backend is open source)

### Claude-Code-Remote
- **URL**: https://github.com/JessyTsui/Claude-Code-Remote
- **Features**: Control via Email, Discord, Telegram, LINE
- **Use case**: Async workflows, notifications when tasks complete
- **Security**: Sender whitelists, session tokens

## Official Options

### Claude iOS App (October 2025)
- Native Claude Code integration
- Runs on Anthropic's cloud VMs (~21GB each)
- Requires Pro/Max subscription
- **Current issues** (per user reports):
  - Freezes when opening keyboard
  - Breaks during screen rotation
  - No image paste support
  - Missing slash command autocomplete
  - "Teleport" handoff feature buggy

### Claude Code on Web
- Browser-based, works on mobile
- Same cloud infrastructure as iOS
- Network domain whitelisting required for external APIs
- No "YOLO mode" to whitelist all domains

## Alternative Workflows

### Asynchronous Planning
- Create markdown to-do lists on phone (Obsidian synced)
- Document plans and context while mobile
- Feed into Claude Code when at desktop
- Works well for ideation during commutes

### GitHub Actions Integration
- Trigger Claude Code workflows via GitHub issues
- Comment on issues to send new commands
- Fully async, no real-time connection needed

### Voice Calling (New Feature)
- Command: `/call "let's discuss the architecture"`
- Claude calls your phone with full context
- Has access to git status, recent commits, todos
- Can read files during call
- Transcripts saved automatically

## Real User Experiences

### Success Stories

> "Shipped a feature from the passenger seat - SSH'd into office desktop, prompted Claude, tested on phone browser, pushed to production in 10 minutes"
> — skeptrune.com

> "I frequently have 2-3 separate Claude Code sessions running at once, often prompted from my phone while walking the dog"
> — HN user

> "Development fits into the gaps of the day instead of requiring dedicated desk time"
> — HN discussion

### Challenges Noted

> "The real bottleneck isn't typing on mobile—it's reviewing the output"

- Testing/validation difficult on phone
- Small screens limit code review
- Work-life balance concerns about always-on expectations
- Official iOS app still early/buggy

## Cost Considerations

| Approach | Cost |
|----------|------|
| SSH + Tailscale + tmux | Free (+ Claude subscription) |
| Happy Coder | Free |
| Claude Code on Web/iOS | ~$7/day in VM costs (built into subscription) |
| Self-hosted VPS | Variable ($5-50/month) |

## Recommendations by Use Case

### Power Users / Full Control
SSH + tmux + Tailscale + Blink Shell (iOS) or Termux (Android)
Add ntfy for notifications, Mosh for unstable connections

### Quick Checks / Light Usage
Official Claude iOS app or Claude Code on Web

### Async / Team Workflows
Claude-Code-Remote (Email/Discord/Telegram) or GitHub Actions integration

### Hands-Free / Voice
Happy Coder with voice input, or new `/call` feature

## Sources

### Mobile Access Guides
- https://blog.esc.sh/using-claude-code-on-the-go/
- https://adim.in/p/remote-control-claude-code/
- https://www.skeptrune.com/posts/claude-code-on-mobile-termux-tailscale/
- https://clay.fyi/blog/iphone-claude-code-context-coding/
- https://every.to/vibe-check/vibe-check-we-spent-a-weekend-trying-to-code-from-our-phones

### Tools
- https://happy.engineering/
- https://github.com/ZohaibAhmed/clauder
- https://github.com/JessyTsui/Claude-Code-Remote

### Hacker News Discussions
- https://news.ycombinator.com/item?id=45787595
- https://news.ycombinator.com/item?id=46491486
- https://news.ycombinator.com/item?id=46507473
- https://news.ycombinator.com/item?id=44878650

### Social
- https://x.com/Bsunter/status/1940249686574866909

### Tailscale & Alternatives
- https://tailscale.com/kb/1151/what-is-tailscale
- https://tailscale.com/blog/how-tailscale-works
- https://pinggy.io/blog/top_open_source_tailscale_alternatives/
- https://wz-it.com/en/blog/netbird-vs-tailscale-comparison/
- https://www.xda-developers.com/switched-from-tailscale-to-fully-self-hosted-alternative-netbird/
- https://github.com/juanfont/headscale
- https://netbird.io/
- https://zerotier.com/
- https://github.com/slackhq/nebula
- https://netmaker.io/
