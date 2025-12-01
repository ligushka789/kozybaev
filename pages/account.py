import streamlit as st
import streamlit.components.v1 as components

def app():
    """
    Account page - пустая страница
    """
    
    vue_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.prod.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            * { font-family: 'Comic Sans MS', 'Comic Sans', cursive !important; }

            body {
                background: linear-gradient(180deg, #8B4C4C 0%, #F5E6D3 100%);
                min-height: 100vh;
                margin: 0;
                padding: 0;
            }
            
            .text-shadow {
                text-shadow: 0px 0px 2px rgba(0,0,0,0.5);
            }
        </style>
    </head>
    <body>
        <div id="app">
            <!-- Header Component -->
            <header-component></header-component>
            
            <!-- Main Content - Пустая страница -->
            <div class="container mx-auto px-4 py-8">
                <div class="text-center text-white text-2xl">
                    <!-- Здесь будет контент страницы My Account -->
                </div>
            </div>
        </div>

        <script>
            const { createApp } = Vue;

            // Header Component
            const HeaderComponent = {
                template: `
                    <div class="h-32 flex items-center justify-center px-10 mb-5">
                        <div class="w-full max-w-7xl flex items-center justify-between">
                            <div class="flex flex-col items-center gap-1">
                                 <div class="w-full max-w-7xl flex items-center justify-between">
                                    
                                </div>
                            </div>
                            
                            <!-- Navigation -->
                            <div class="w-full max-w-7xl grid grid-cols-3 items-center">

                                <!-- LEFT: HOME -->
                                <div class="flex justify-start">
                                    <button @click="navigate('home')" 
                                        class="text-white text-xl font-semibold text-shadow hover:opacity-80 transition">
                                        Home
                                    </button>
                                </div>

                                <!-- CENTER: LOGO -->
                                <div class="flex justify-center">
                                    <img src="data:image/png;base64,...." 
                                        class="w-48 h-auto cursor-pointer"
                                        @click="navigate('home')" />
                                </div>

                                <!-- RIGHT: DROPDOWN + ACCOUNT -->
                                <div class="flex justify-end items-center gap-6">

                                    <!-- DROPDOWN -->
                                    <div class="relative" 
                                         @mouseenter="showMoreMenu = true" 
                                         @mouseleave="showMoreMenu = false">
                                        <button class="text-white text-xl font-semibold text-shadow hover:opacity-80 transition">
                                            More ▾
                                        </button>

                                        <transition name="fade">
                                            <div v-if="showMoreMenu" 
                                                 class="absolute right-0 mt-2 bg-white rounded-xl shadow-lg overflow-hidden z-50 min-w-[180px]">

                                                <button @click="navigate('stats')" class="block px-4 py-2 text-left hover:bg-gray-100 w-full">
                                                    Statistics
                                                </button>

                                                <button @click="navigate('datasets')" class="block px-4 py-2 text-left hover:bg-gray-100 w-full">
                                                    Datasets
                                                </button>

                                                <button @click="navigate('faq')" class="block px-4 py-2 text-left hover:bg-gray-100 w-full text-red-500 font-semibold">
                                                    FAQ
                                                </button>

                                                <button @click="navigate('about')" class="block px-4 py-2 text-left hover:bg-gray-100 w-full">
                                                    About us
                                                </button>
                                            </div>
                                        </transition>
                                    </div>

                                    <!-- ACCOUNT -->
                                    <button @click="navigate('account')" 
                                            class="text-white text-xl font-semibold text-shadow hover:opacity-80 transition">
                                        My Account →
                                    </button>

                                </div>

                            </div>

                        </div>
                    </div>
                    <hr class="border-white/20 mb-8">
                `,
                data() {
                    return {
                        showMoreMenu: false
                    }
                },
                methods: {
                    navigate(page) {
                        window.location.href = `?page=${page}`;
                    }
                }
            };

            createApp({
                components: {
                    'header-component': HeaderComponent
                },
                data() {
                    return {}
                }
            }).mount('#app');
        </script>
    </body>
    </html>
    """
    components.html(vue_html, height=1000, scrolling=True)