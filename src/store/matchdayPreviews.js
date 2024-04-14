import { defineStore } from 'pinia'
import { getAuth } from 'firebase/auth'
import { onSnapshot, doc, collection, query, addDoc, setDoc, updateDoc, deleteDoc, getDoc, getDocs } from 'firebase/firestore'

import { db } from '@/plugins/firebase'

let binding = null

export const useMatchdayPreviewsStore = defineStore('matchdayPreviews', {
  state: () => ({
    all: []
  }),
  getters: {
    getAll: (state) => state.all,
    getByID: (state) => {
      return (id) => state.all.find((rec) => rec.id === id)
    },
    getAllSortedByKickoff: (state) => {
      return state.all.sort((a, b) => {
        return a.kickoff?.toDate() - b.kickoff?.toDate()
      })
    },
    getAllSortedByCreatedTimestamp: (state) => {
      return state.all.sort((a, b) => {
        return a.createdTimestamp?.toDate() - b.createdTimestamp?.toDate()
      })
    },
  },
  actions: {
    ////////////// REALTIME CONNECTION //////////////
    bind() {
      const q = query(collection(db, "matchday-previews"))
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
    // Fetch all matchday-previews
    async fetchAll() {
      const q = query(collection(db, "matchday-previews"))
      const querySnapshot = await getDocs(q)
      this.all = []
      querySnapshot.forEach((doc) => {
        this.all.push({id: doc.id, ...doc.data()})
      })
    },
    async fetchSingle(id) {
      const docRef = doc(db, "matchday-previews", id)
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

    // add matchday-preview
    async add(payload) {
      const docRef = collection(db, "matchday-previews")
      await addDoc(docRef, payload)
        .catch((error) => {
          console.error(error)
          throw error
        })
    },

    // update matchday-preview
    async update(id, myPayload) {
      const docRef = doc(db, "matchday-previews", id)
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

    // set matchday-preview
    async set(id, myPayload, merge=true) {
      const docRef = doc(db, "matchday-previews", id)
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

    // delete matchday-preview
    async delete(id, myPayload) {
      const docRef = doc(db, "matchday-previews", id)
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
