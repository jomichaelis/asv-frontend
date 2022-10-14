import { vuexfireMutations, firestoreAction } from 'vuexfire'

export const state = () => ({
    matchdayImages: []
})

export const getters = {
    all: (state) => {
        return state.matchdayImages
    },
    byID: (state) => {
        return id => state.matchdayImages.find(doc => doc.id === id)
    }
}

export const mutations = {
    ...vuexfireMutations,
}

export const actions = {
    bindMatchdayImages: firestoreAction(function ({ bindFirestoreRef }) {
        return bindFirestoreRef('matchdayImages', this.$fire.firestore.collection('matchday-preview'))
    }),
    unbindMatchdayImages: firestoreAction(({ unbindFirestoreRef }) => {
        return unbindFirestoreRef('matchdayImages')
    })
}
