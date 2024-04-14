import { defineStore } from 'pinia'
import { getAuth } from 'firebase/auth'
import { onSnapshot, doc, collection, query, addDoc, setDoc, updateDoc, deleteDoc, getDoc, getDocs } from 'firebase/firestore'

import { db } from '@/plugins/firebase'

let binding = null

export const useTeamsStore = defineStore('teams', {
  state: () => ({
    all: []
  }),
  getters: {
    getAll: (state) => state.all,
    getByID: (state) => {
      return (id) => state.all.find((rec) => rec.id === id)
    },
    getAllSortedByName: (state) => {
      return state.all.sort((a, b) => {
        return a.name?.localeCompare(b.name)
      })
    },
    getAllSorted: (state) => {
      return state.all.filter(team => team.isASV)?.sort((a, b) => {
        return b.order - a.order
      })
    }
  },
  actions: {
    ////////////// REALTIME CONNECTION //////////////
    bind() {
      const q = query(collection(db, "teams"))
      binding = onSnapshot(q, (querySnapshot) => {
        this.all = []
        querySnapshot.forEach((doc) => {
          this.all.push({id: doc.id, ...doc.data()})
        })
      })
    },
    unbind() {
      if(binding) binding()
    },
    /////////////////////////////////////////////////
    // Fetch all teams
    async fetchAll() {
      const q = query(collection(db, "teams"))
      const querySnapshot = await getDocs(q)
      this.all = []
      querySnapshot.forEach((doc) => {
        this.all.push({id: doc.id, ...doc.data()})
      })
    },
    async fetchTeam(id) {
      const docRef = doc(db, "teams", id)
      const docSnap = await getDoc(docRef)
      if (docSnap.exists()) {
        if(this.all.find((team) => team.id === docSnap.id)) {
          const index = this.all.findIndex((team) => team.id === docSnap.id)
          this.all[index] = {id: docSnap.id, ...docSnap.data()}
        } else {
          this.all.push({id: docSnap.id, ...docSnap.data()})
        }
      } else {
        console.error("No such document!")
      }
    },

    // add team
    async addTeam(payload) {
      const docRef = collection(db, "teams")
      await addDoc(docRef, payload)
        .catch((error) => {
          console.error(error)
          throw error
        })
    },

    // update team
    async updateTeam(id, myPayload) {
      const docRef = doc(db, "teams", id)
      const payload = {
        ...myPayload,
        updatedTimestamp: new Date(),
        updatedUserID: getAuth().currentUser.uid
      }
      await updateDoc(docRef, payload, { merge: true })
        .catch((error) => {
          console.error(error)
          throw error
        })
    },

    // set team
    async setTeam(id, myPayload, merge=true) {
      const docRef = doc(db, "teams", id)
      const payload = {
        ...myPayload,
        updatedTimestamp: new Date(),
        updatedUserID: getAuth().currentUser.uid
      }
      await setDoc(docRef, payload, { merge: merge })
        .catch((error) => {
          console.error(error)
          throw error
        })
    },

    // delete team
    async deleteTeam(id, myPayload) {
      const docRef = doc(db, "teams", id)
      const payload = {
        ...myPayload,
        updatedTimestamp: new Date(),
        updatedUserID: getAuth().currentUser.uid
      }
      await deleteDoc(docRef)
        .catch((error) => {
          console.error(error)
          throw error
        })
    },

  }
})
