package main

import "fmt"

type Stat int

func (s Stat) IsValid() bool {
	return s >= 0 && s <= 9
}

type StatsValues struct {
	Range              float32
	Speed              float32
	BulletSpeed        float32
	BulletTTL          float32
	BulletDamage       float32
	HealthMax          float32
	HealthRegeneration float32
	BodyDamage         float32
	ReloadSpeed        int
}

type Stats struct {
	Range              int `json:"range"`
	Speed              int `json:"speed"`
	BulletSpeed        int `json:"bullet_speed"`
	BulletTTL          int `json:"bullet_ttl"`
	BulletDamage       int `json:"bullet_damage"`
	HealthMax          int `json:"health_max"`
	HealthRegeneration int `json:"health_regeneration"`
	BodyDamage         int `json:"body_damage"`
	ReloadSpeed        int `json:"reload_speed"`
}

func (p *Player) UpgradeStat(stat Stat) error {
	if !stat.IsValid() {
		return fmt.Errorf("unknown stat %d", stat)
	}

	if stat == StatNone {
		return fmt.Errorf("no stat to upgrade")
	}

	if p.LevelsLeft <= 0 {
		return fmt.Errorf("not enough levels left (%d < 1)", p.LevelsLeft)
	}

	switch stat {
	case StatRange:
		if len(RangeValues)-1 > p.Stats.Range {
			p.Stats.Range++
		} else {
			return fmt.Errorf("the stat 'Range' is already at the highest level")
		}
		break
	case StatSpeed:
		if len(SpeedValues)-1 > p.Stats.Speed {
			p.Stats.Speed++
		} else {
			return fmt.Errorf("the stat 'Speed' is already at the highest level")
		}
		break
	case StatBulletSpeed:
		if len(BulletSpeedValues)-1 > p.Stats.BulletSpeed {
			p.Stats.BulletSpeed++
		} else {
			return fmt.Errorf("the stat 'BulletSpeed' is already at the highest level")
		}
		break
	case StatBulletTTL:
		if len(BulletTTLValues)-1 > p.Stats.BulletTTL {
			p.Stats.BulletTTL++
		} else {
			return fmt.Errorf("the stat 'BulletTTL' is already at the highest level")
		}
		break
	case StatBulletDamage:
		if len(BulletDamageValues)-1 > p.Stats.BulletDamage {
			p.Stats.BulletDamage++
		} else {
			return fmt.Errorf("the stat 'BulletDamage' is already at the highest level")
		}
		break
	case StatHealthMax:
		if len(HealthMaxValues)-1 > p.Stats.HealthMax {
			p.Stats.HealthMax++
		} else {
			return fmt.Errorf("the stat 'HealthMax' is already at the highest level")
		}
		break
	case StatHealthRegeneration:
		if len(HealthRegenerationValues)-1 > p.Stats.HealthRegeneration {
			p.Stats.HealthRegeneration++
		} else {
			return fmt.Errorf("the stat 'HealthRegeneration' is already at the highest level")
		}
		break
	case StatBodyDamage:
		if len(BodyDamageValues)-1 > p.Stats.BodyDamage {
			p.Stats.BodyDamage++
		} else {
			return fmt.Errorf("the stat 'BodyDamage' is already at the highest level")
		}
		break
	case StatReloadSpeed:
		if len(ReloadSpeedValues)-1 > p.Stats.ReloadSpeed {
			p.Stats.ReloadSpeed++
		} else {
			return fmt.Errorf("the stat 'ReloadSpeed' is already at the highest level")
		}
		break
	}

	p.LevelsLeft--
	return nil
}
