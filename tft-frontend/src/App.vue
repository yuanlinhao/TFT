<template>
  <div>
    <h1>TFT Damage Calculator</h1>

    <!-- Champion Selection -->
    <h2>Select Champion</h2>
    <select v-model="selectedChampion">
      <option v-for="champ in champions" :key="champ.id" :value="champ">
        {{ champ.name }}
      </option>
    </select>

    <!-- Item Selection -->
    <h2>Select Items</h2>
    <div v-for="(item, index) in selectedItems" :key="index">
      <select v-model="selectedItems[index]">
        <option v-for="itm in items" :key="itm.id" :value="itm">
          {{ itm.name }}
        </option>
      </select>
    </div>
    
    <button @click="calculateDamage">Calculate Damage</button>

    <!-- Display Results -->
    <h2>Damage Output</h2>
    <p v-if="damageResults">
      Auto Attack Damage: {{ damageResults.autoAttackDamage }} <br />
      Ability Damage: {{ damageResults.abilityDamage }} <br />
      Critical Auto Attack: {{ damageResults.critAutoAttackDamage }} <br />
      Critical Ability Damage: {{ damageResults.critAbilityDamage }}
    </p>
  </div>
</template>

<script>
import { fetchChampions, fetchItems } from './services/api';

export default {
  data() {
    return {
      champions: [],
      items: [],
      selectedChampion: null,
      selectedItems: [{}, {}, {}], // TFT allows 3 items
      damageResults: null,
    };
  },
  async mounted() {
    this.champions = await fetchChampions();
    this.items = await fetchItems();
  },
  methods: {
    extractAbilityDamage(description) {
      const match = description.match(/\d+/); // Extracts first number found
      return match ? parseInt(match[0]) : 0;
    },

    calculateDamage() {
      if (!this.selectedChampion) return;

      let { attack_damage, ability_description } = this.selectedChampion;
      let abilityDamage = this.extractAbilityDamage(ability_description); // Parse from description
      let critChance = 0;
      let critDamage = 1.5; // Default crit multiplier
      let bonusAP = 0;

      // Apply item effects
      this.selectedItems.forEach(item => {
        if (item && item.name) {
          if (item.ability_power) bonusAP += item.ability_power;
          if (item.crit_chance) critChance += item.crit_chance;
          if (item.crit_damage) critDamage += item.crit_damage;
        }
      });

      // Crit Scaling if critChance exceeds 100%
      if (critChance > 1) {
        critDamage += (critChance - 1);
        critChance = 1; // Cap at 100% chance
      }

      // Calculate final damage
      let autoAttackDamage = attack_damage;
      let critAutoAttackDamage = attack_damage * critDamage;
      let scaledAbilityDamage = abilityDamage * (1 + bonusAP / 100);
      let critAbilityDamage = scaledAbilityDamage * critDamage;

      this.damageResults = {
        autoAttackDamage: autoAttackDamage.toFixed(2),
        abilityDamage: scaledAbilityDamage.toFixed(2),
        critAutoAttackDamage: critAutoAttackDamage.toFixed(2),
        critAbilityDamage: critAbilityDamage.toFixed(2),
      };
    }
  }
};
</script>
