import { defineStore } from 'pinia'
import { getAuth } from 'firebase/auth'
import { onSnapshot, doc, collection, query, addDoc, setDoc, updateDoc, deleteDoc, getDoc, getDocs } from 'firebase/firestore'

import { db } from '@/plugins/firebase'

let binding = null

export const useUpcomingMatchesStore = defineStore('upcoming-matches', {
  state: () => ({
    all: []
  }),
  getters: {
    getAll: (state) => state.all,
    getByID: (state) => {
      return (id) => state.all.find((rec) => rec.id === id)
    },
  },
  actions: {
    ////////////// REALTIME CONNECTION //////////////
    bind() {
      const q = query(collection(db, "upcoming_matches"))
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
    // Fetch all upcoming matches
    async fetchAll() {
      const q = query(collection(db, "upcoming_matches"))
      const querySnapshot = await getDocs(q)
      this.all = []
      querySnapshot.forEach((doc) => {
        this.all.push({id: doc.id, ...doc.data()})
      })
    },
    async fetchSingle(id) {
      const docRef = doc(db, "upcoming_matches", id)
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

    // add upcoming match
    async add(payload) {
      const docRef = collection(db, "upcoming_matches")
      await addDoc(docRef, payload)
        .catch((error) => {
          console.error(error)
          throw error
        })
    },

    // update upcoming match
    async update(id, myPayload) {
      const docRef = doc(db, "upcoming_matches", id)
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

    // set upcoming match
    async set(id, myPayload, merge=true) {
      const docRef = doc(db, "upcoming_matches", id)
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

    // delete upcoming match
    async deleteTeam(id, myPayload) {
      const docRef = doc(db, "upcoming_matches", id)
      await deleteDoc(docRef)
        .catch((error) => {
          console.error(error)
          throw error
        })
    },

  }
})
