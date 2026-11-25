# GasFeeLoop- (legacy GFLO contracts) — DEPRECATED

> **Status: DEPRECATED / legacy, as of 2026-11-25.** Do not build on these contracts,
> integrate them, or treat them as the current GFLO protocol. They remain on
> Sepolia only as a historical record.

## Legacy Sepolia deployments

| Contract | Sepolia address | Note |
| --- | --- | --- |
| GFLOToken | `0x563b2e3b499818a2f84c472efb3169a2667807fe` | ERC-20, legacy commitment token |
| PIECore v3 | `0x9CF55d0b9D61Dc28EF3cb10765CF4b861Cd0991e` | **Known issue:** `gainXP()` has no authorization check — any caller can mint XP to itself |
| GFLOIgnition | `0x414DEDcf9264614Fd087BDa58bE27a0B698CcC54` | Calls `upgradeTier(address)` on PIECore (not `addXP()`); legacy burn-for-tier design |
| GasFeeLoop | `0xd2C926F67080D6315b5dbBc7D621d729Cfe8A9C7` | Legacy stake / XP multiplier |

All four have source verified on Sepolia Etherscan. Their XP and tier values carry
no meaning in the current protocol and must not be migrated or read as reputation.

## Why deprecated

- The PIECore v3 `gainXP()` authorization gap makes every XP and tier value untrustworthy.
- The burn-for-tier model (GFLOIgnition) conflicts with the current principle:
  *money buys capacity, never standing*. It is replaced by XP + time based tier
  progression (`TierProgressionV01`, DESIGN-004).
- This repository's `contracts/core/PIECore.sol` does not match the deployed PIECore v3 bytecode.

## Where the current protocol lives

- **Canonical PIE / PoVA:** [elanmust-GFLOer/gflo-pie](https://github.com/elanmust-GFLOer/gflo-pie)
  (`main`, v0.2 with DESIGN-003/004/005).
- No current GFLO contract is deployed on a public network. Base Sepolia: BLOCK;
  production: NO-GO.

## Magyarul

**Elavult (2026-11-25).** A fenti négy Sepolia-kontraktus csak történeti nyilvántartásként
marad. Ne építs rájuk, és XP/tier értékeiket ne kezeld reputációként: a PIECore v3
`gainXP()` függvényéből hiányzik a jogosultság-ellenőrzés. A kanonikus protokoll a
[gflo-pie](https://github.com/elanmust-GFLOer/gflo-pie) repóban van.
