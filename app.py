import streamlit as st
import streamlit.components.v1 as components
import json
from curiosita import testi_curiosita

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Verifica: Paleolitico e Neolitico", layout="wide")

st.title("🏹 Scopriamo la Preistoria!")
st.markdown("Trascina gli oggetti e le abitudini nel periodo storico corretto. Aiuta l'uomo del Paleolitico e la donna del Neolitico a ritrovare le loro cose!")

# === IL CUORE DEL GIOCO: HTML, CSS e JS INIETTATI ===
custom_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');
        
        body {
            font-family: 'Comic Neue', cursive, sans-serif;
            background-color: #f0f8ff;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .game-board {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 1000px;
            margin-bottom: 40px;
        }

        /* Le due zone in cui trascinare gli oggetti */
        .drop-zone {
            width: 68%;
            min-height: 280px;
            background-color: #ffffff;
            border: 4px dashed #ccc;
            border-radius: 20px;
            padding: 15px;
            display: flex;
            flex-wrap: wrap;
            align-content: flex-start;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .drop-zone.dragover {
            background-color: #e6ffe6;
            border-color: #4CAF50;
            transform: scale(1.02);
        }

        /* Intestazioni delle drop zone (I personaggi) */
        .character-header {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #eee;
            width: 100%;
            display: block;
        }

        .character-header h2 {
            color: #333;
            margin: 10px 0 0 0;
            font-size: 24px;
        }

        .char-placeholder {
            font-size: 60px;
            background: #f1f1f1;
            border-radius: 50%;
            width: 120px;
            height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
        }

        /* Area contenitore degli oggetti da smistare */
        .items-pool {
            width: 100%;
            max-width: 1000px;
            background-color: #fff9c4;
            border: 4px solid #fbc02d;
            border-radius: 20px;
            padding: 30px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            min-height: 250px;
        }

        /* Il singolo oggetto trascinabile */
        .draggable-item {
            background-color: white;
            border: 3px solid #ddd;
            border-radius: 12px;
            padding: 10px;
            width: 130px;
            text-align: center;
            cursor: grab;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }

        .draggable-item:active {
            cursor: grabbing;
        }

        .draggable-item:hover {
            transform: translateY(-5px);
            border-color: #2196F3;
        }

        .draggable-item svg {
            width: 70px;
            height: 70px;
            margin-bottom: 8px;
        }

        .draggable-item span {
            font-size: 15px;
            color: #444;
            line-height: 1.2;
        }

        /* Quando l'oggetto è posizionato correttamente */
        .drop-zone .draggable-item {
            margin: 8px;
            cursor: pointer;
            border-color: #4CAF50;
            background-color: #f1f8e9;
        }
        
        /* Simbolino che indica che si può cliccare */
        .drop-zone .draggable-item::after {
            content: "💡Clicca!";
            position: absolute;
            top: -10px;
            right: -10px;
            background: #FFEB3B;
            border-radius: 10px;
            padding: 2px 6px;
            font-size: 12px;
            border: 2px solid #FBC02D;
            animation: bounce 1.5s infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }

        /* STILE DEL POP-UP (MODAL) CURIOSITA' */
        .modal {
            display: none;
            position: fixed;
            z-index: 100;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            align-items: center;
            justify-content: center;
        }

        .modal-content {
            background-color: #fff;
            padding: 30px;
            border-radius: 20px;
            border: 5px solid #2196F3;
            width: 80%;
            max-width: 500px;
            text-align: center;
            position: relative;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            animation: popin 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes popin {
            from { transform: scale(0.5); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        .close-btn {
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 30px;
            font-weight: bold;
            color: #f44336;
            cursor: pointer;
        }

        .modal-content h3 {
            color: #FF9800;
            font-size: 28px;
            margin-top: 0;
        }

        .modal-content p {
            font-size: 20px;
            color: #444;
            line-height: 1.4;
        }
    </style>
</head>
<body>

    <!-- IL POP-UP LO SAPEVI CHE -->
    <div id="info-modal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <h3>✨ Lo sapevi che? ✨</h3>
            <p id="modal-text">Qui andrà la curiosità...</p>
        </div>
    </div>

    <!-- IL TABELLONE DI GIOCO CON I PERSONAGGI -->
    <div class="game-board">
        <!-- Zona Paleolitico -->
        <div class="drop-zone" id="zone-paleolitico">
            <div class="character-header">
                <div class="char-placeholder" style="background: transparent;">
                    <svg viewBox="0 0 100 100" style="width: 100%; height: 100%;">
                        <!-- Lancia dietro la schiena -->
                        <line x1="20" y1="90" x2="80" y2="20" stroke="#795548" stroke-width="4" stroke-linecap="round"/>
                        <polygon points="75,25 85,15 88,25" fill="#9E9E9E"/>

                        <!-- Corpo e vestito di pelli -->
                        <path d="M 35 90 C 35 60, 40 50, 50 50 C 60 50, 65 60, 65 90 Z" fill="#8D6E63"/>
                        <!-- Macchioline stile leopardo -->
                        <circle cx="45" cy="65" r="3" fill="#4E342E"/>
                        <circle cx="58" cy="75" r="4" fill="#4E342E"/>
                        <circle cx="42" cy="82" r="2.5" fill="#4E342E"/>
                        <circle cx="55" cy="58" r="2" fill="#4E342E"/>

                        <!-- Braccia -->
                        <path d="M 38 55 Q 25 70 30 80" stroke="#FFBCA5" stroke-width="6" stroke-linecap="round" fill="none"/>
                        <path d="M 62 55 Q 75 70 70 80" stroke="#FFBCA5" stroke-width="6" stroke-linecap="round" fill="none"/>

                        <!-- Testa rotonda -->
                        <circle cx="50" cy="35" r="22" fill="#FFBCA5"/>
                        
                        <!-- Capelli arruffati -->
                        <path d="M 25 35 C 20 15, 80 15, 75 35 C 80 20, 50 5, 25 35 Z" fill="#5D4037"/>
                        <polygon points="30,25 35,35 40,22 50,32 55,20 65,32 70,25" fill="#4E342E"/>

                        <!-- Occhioni grandi e simpatici -->
                        <circle cx="41" cy="35" r="4.5" fill="#212121"/>
                        <circle cx="42" cy="33.5" r="1.5" fill="#FFFFFF"/>
                        <circle cx="59" cy="35" r="4.5" fill="#212121"/>
                        <circle cx="60" cy="33.5" r="1.5" fill="#FFFFFF"/>

                        <!-- Guancette rosse -->
                        <ellipse cx="33" cy="40" rx="3.5" ry="2" fill="#FF8A65" opacity="0.7"/>
                        <ellipse cx="67" cy="40" rx="3.5" ry="2" fill="#FF8A65" opacity="0.7"/>

                        <!-- Sorrisone -->
                        <path d="M 45 42 Q 50 48 55 42" stroke="#212121" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                    </svg>
                </div>
                <h2>Paleolitico</h2>
                <small>Età della pietra antica</small>
            </div>
            <!-- Gli oggetti corretti verranno spostati qui da JS -->
        </div>

        <!-- Zona Neolitico -->
        <div class="drop-zone" id="zone-neolitico">
            <div class="character-header">
                <div class="char-placeholder" style="background: transparent;">
                    <svg viewBox="0 0 100 100" style="width: 100%; height: 100%;">
                        <!-- Corpo e vestito in tessuto -->
                        <path d="M 30 90 C 35 60, 40 50, 50 50 C 60 50, 65 60, 70 90 Z" fill="#A5D6A7"/>
                        
                        <!-- Decorazione del vestito (strisce) -->
                        <path d="M 37 70 Q 50 75 63 70" stroke="#81C784" stroke-width="3" fill="none"/>
                        <path d="M 34 80 Q 50 85 66 80" stroke="#81C784" stroke-width="3" fill="none"/>

                        <!-- Braccia -->
                        <path d="M 38 55 Q 20 60 30 75" stroke="#FFCCBC" stroke-width="5" stroke-linecap="round" fill="none"/>
                        <path d="M 62 55 Q 80 60 70 75" stroke="#FFCCBC" stroke-width="5" stroke-linecap="round" fill="none"/>

                        <!-- Piccolo vasetto in mano -->
                        <ellipse cx="73" cy="73" rx="8" ry="10" fill="#D84315"/>
                        <ellipse cx="73" cy="63" rx="5" ry="2" fill="#BF360C"/>
                        <path d="M 68 63 L 78 63 L 75 68 L 71 68 Z" fill="#D84315"/>

                        <!-- Testa rotonda -->
                        <circle cx="50" cy="35" r="20" fill="#FFCCBC"/>
                        
                        <!-- Capelli raccolti (codini/chignon) -->
                        <circle cx="30" cy="45" r="7" fill="#424242"/> 
                        <circle cx="70" cy="45" r="7" fill="#424242"/>
                        <path d="M 28 35 C 30 10, 70 10, 72 35 C 65 20, 35 20, 28 35 Z" fill="#212121"/>
                        
                        <!-- Fascia per capelli colorata -->
                        <path d="M 31 28 Q 50 35 69 28" stroke="#81C784" stroke-width="3" fill="none"/>

                        <!-- Occhioni dolci con ciglia -->
                        <circle cx="42" cy="36" r="4" fill="#212121"/>
                        <circle cx="43" cy="34.5" r="1.5" fill="#FFFFFF"/>
                        <line x1="38" y1="34" x2="35" y2="31" stroke="#212121" stroke-width="1.5" stroke-linecap="round"/>
                        
                        <circle cx="58" cy="36" r="4" fill="#212121"/>
                        <circle cx="59" cy="34.5" r="1.5" fill="#FFFFFF"/>
                        <line x1="62" y1="34" x2="65" y2="31" stroke="#212121" stroke-width="1.5" stroke-linecap="round"/>

                        <!-- Guancette rosse -->
                        <ellipse cx="35" cy="41" rx="3.5" ry="2" fill="#FF8A65" opacity="0.7"/>
                        <ellipse cx="65" cy="41" rx="3.5" ry="2" fill="#FF8A65" opacity="0.7"/>

                        <!-- Sorriso dolce -->
                        <path d="M 46 43 Q 50 47 54 43" stroke="#212121" stroke-width="2" fill="none" stroke-linecap="round"/>
                    </svg>
                </div>
                <h2>Neolitico</h2>
                <small>Età della pietra nuova</small>
            </div>
            <!-- Gli oggetti corretti verranno spostati qui da JS -->
        </div>
    </div>

    <h3 style="color: #666; margin-bottom: 10px;">Scatola degli oggetti (Trascinali su!)</h3>
    
    <!-- Zona Oggetti Iniziali -->
    <div class="items-pool" id="items-pool">
        
        <!-- PALEOLITICO: Capanna di pelli -->
        <div class="draggable-item" draggable="true" id="item_pal_1" data-era="zone-paleolitico">
            <svg viewBox="0 0 100 100">
                <path d="M50 10 L20 80 L80 80 Z" fill="#8B4513" stroke="#5C3A21" stroke-width="4"/>
                <path d="M50 10 L50 80" stroke="#5C3A21" stroke-width="2" stroke-dasharray="4,4"/>
                <path d="M40 80 L50 60 L60 80 Z" fill="#3E2723"/>
            </svg>
            <span>Capanna smontabile</span>
        </div>

        <!-- NEOLITICO: Agricoltura -->
        <div class="draggable-item" draggable="true" id="item_neo_1" data-era="zone-neolitico">
            <svg viewBox="0 0 100 100">
                <path d="M50 90 L50 20" stroke="#4CAF50" stroke-width="4" fill="none"/>
                <path d="M50 40 Q40 30 50 20 Q60 30 50 40" fill="#FFC107"/>
                <path d="M50 55 Q35 45 50 35 Q65 45 50 55" fill="#FFC107"/>
                <path d="M50 70 Q30 60 50 50 Q70 60 50 70" fill="#FFC107"/>
            </svg>
            <span>Agricoltura</span>
        </div>

        <!-- PALEOLITICO: Caccia (Omino + Mammut) -->
        <div class="draggable-item" draggable="true" id="item_pal_2" data-era="zone-paleolitico">
            <svg viewBox="0 0 100 100">
                <circle cx="20" cy="40" r="5" fill="#333"/>
                <line x1="20" y1="45" x2="20" y2="65" stroke="#333" stroke-width="2"/>
                <line x1="20" y1="50" x2="40" y2="45" stroke="#333" stroke-width="2"/>
                <line x1="10" y1="75" x2="20" y2="65" stroke="#333" stroke-width="2"/>
                <line x1="30" y1="75" x2="20" y2="65" stroke="#333" stroke-width="2"/>
                <line x1="15" y1="50" x2="55" y2="35" stroke="#795548" stroke-width="2"/>
                <ellipse cx="70" cy="55" rx="20" ry="15" fill="#795548"/>
                <circle cx="60" cy="45" r="10" fill="#795548"/>
                <path d="M50 45 Q40 55 45 70" fill="none" stroke="#795548" stroke-width="4"/>
                <path d="M55 45 Q45 40 40 35" fill="none" stroke="#FFF" stroke-width="2"/>
                <line x1="65" y1="70" x2="65" y2="80" stroke="#795548" stroke-width="6"/>
                <line x1="75" y1="70" x2="75" y2="80" stroke="#795548" stroke-width="6"/>
            </svg>
            <span>Caccia grossa</span>
        </div>

        <!-- NEOLITICO: Vaso Ceramica -->
        <div class="draggable-item" draggable="true" id="item_neo_2" data-era="zone-neolitico">
            <svg viewBox="0 0 100 100">
                <path d="M35 30 L65 30 L60 40 C 80 50, 80 80, 50 80 C 20 80, 20 50, 40 40 Z" fill="#D84315" stroke="#BF360C" stroke-width="2"/>
                <ellipse cx="50" cy="30" rx="15" ry="5" fill="#BF360C"/>
                <path d="M30 60 L40 50 L50 60 L60 50 L70 60" stroke="#FFCC80" stroke-width="2" fill="none"/>
            </svg>
            <span>Vaso di ceramica</span>
        </div>

        <!-- PALEOLITICO: Raccolta -->
        <div class="draggable-item" draggable="true" id="item_pal_3" data-era="zone-paleolitico">
            <svg viewBox="0 0 100 100">
                <path d="M20 60 Q50 90 80 60 Z" fill="#8D6E63" stroke="#5D4037" stroke-width="2"/>
                <circle cx="35" cy="55" r="8" fill="#E53935"/>
                <circle cx="50" cy="50" r="10" fill="#E53935"/>
                <circle cx="65" cy="55" r="8" fill="#E53935"/>
                <path d="M50 50 Q50 20 70 20" stroke="#4CAF50" stroke-width="4" fill="none" stroke-linecap="round"/>
                <path d="M35 55 Q30 30 45 25" stroke="#4CAF50" stroke-width="3" fill="none" stroke-linecap="round"/>
            </svg>
            <span>Raccolta (Frutti e radici)</span>
        </div>

        <!-- NEOLITICO: Casa Mattoni -->
        <div class="draggable-item" draggable="true" id="item_neo_3" data-era="zone-neolitico">
            <svg viewBox="0 0 100 100">
                <rect x="25" y="45" width="50" height="45" fill="#E0E0E0" stroke="#9E9E9E" stroke-width="2"/>
                <line x1="25" y1="60" x2="75" y2="60" stroke="#9E9E9E" stroke-width="2"/>
                <line x1="25" y1="75" x2="75" y2="75" stroke="#9E9E9E" stroke-width="2"/>
                <line x1="40" y1="45" x2="40" y2="90" stroke="#9E9E9E" stroke-width="2" stroke-dasharray="15 15"/>
                <line x1="60" y1="45" x2="60" y2="90" stroke="#9E9E9E" stroke-width="2" stroke-dasharray="15 15"/>
                <path d="M15 45 L85 45 L85 30 L15 30 Z" fill="#795548"/>
                <rect x="40" y="65" width="20" height="25" fill="#5D4037"/>
            </svg>
            <span>Casa in mattoni</span>
        </div>

        <!-- PALEOLITICO: Amigdala -->
        <div class="draggable-item" draggable="true" id="item_pal_4" data-era="zone-paleolitico">
            <svg viewBox="0 0 100 100">
                <path d="M50 15 C 70 40, 80 80, 50 85 C 20 80, 30 40, 50 15 Z" fill="#9E9E9E" stroke="#616161" stroke-width="3" stroke-linejoin="round"/>
                <path d="M50 15 L50 85 M35 50 L65 50" stroke="#757575" stroke-width="2" stroke-dasharray="5 5"/>
            </svg>
            <span>Pietra scheggiata</span>
        </div>

        <!-- NEOLITICO: Allevamento -->
        <div class="draggable-item" draggable="true" id="item_neo_4" data-era="zone-neolitico">
            <svg viewBox="0 0 100 100">
                <path d="M10 60 L90 60 M10 75 L90 75 M20 50 L20 85 M50 50 L50 85 M80 50 L80 85" stroke="#795548" stroke-width="4" stroke-linecap="round"/>
                <ellipse cx="50" cy="45" rx="22" ry="16" fill="#F5F5F5" stroke="#E0E0E0" stroke-width="2"/>
                <circle cx="30" cy="40" r="8" fill="#E0E0E0"/>
                <line x1="38" y1="60" x2="38" y2="70" stroke="#424242" stroke-width="3"/>
                <line x1="62" y1="60" x2="62" y2="70" stroke="#424242" stroke-width="3"/>
            </svg>
            <span>Allevamento</span>
        </div>

        <!-- PALEOLITICO: Fuoco -->
        <div class="draggable-item" draggable="true" id="item_pal_5" data-era="zone-paleolitico">
            <svg viewBox="0 0 100 100">
                <line x1="25" y1="85" x2="75" y2="85" stroke="#5D4037" stroke-width="8" stroke-linecap="round"/>
                <line x1="35" y1="90" x2="65" y2="75" stroke="#4E342E" stroke-width="8" stroke-linecap="round"/>
                <path d="M50 80 C 20 50, 40 20, 50 10 C 60 20, 80 50, 50 80 Z" fill="#FF9800"/>
                <path d="M50 80 C 35 60, 45 40, 50 30 C 55 40, 65 60, 50 80 Z" fill="#FFEB3B"/>
            </svg>
            <span>Fuoco per il clan</span>
        </div>

        <!-- NEOLITICO: Ascia Levigata -->
        <div class="draggable-item" draggable="true" id="item_neo_5" data-era="zone-neolitico">
            <svg viewBox="0 0 100 100">
                <line x1="20" y1="80" x2="65" y2="35" stroke="#8D6E63" stroke-width="8" stroke-linecap="round"/>
                <path d="M55 25 L80 50 C 70 65, 55 65, 45 40 Z" fill="#4DB6AC" stroke="#00796B" stroke-width="2"/>
                <line x1="50" y1="40" x2="65" y2="55" stroke="#8D6E63" stroke-width="4"/>
            </svg>
            <span>Pietra levigata</span>
        </div>

        <!-- PALEOLITICO: Grotta -->
        <div class="draggable-item" draggable="true" id="item_pal_6" data-era="zone-paleolitico">
            <svg viewBox="0 0 100 100">
                <path d="M10 90 C 10 30, 90 30, 90 90 Z" fill="#9E9E9E"/>
                <path d="M30 90 C 30 50, 70 50, 70 90 Z" fill="#424242"/>
                <circle cx="25" cy="70" r="5" fill="#757575"/>
                <circle cx="80" cy="80" r="6" fill="#757575"/>
            </svg>
            <span>Rifugio in grotta</span>
        </div>

        <!-- NEOLITICO: Villaggio (Case di Mattoni) -->
        <div class="draggable-item" draggable="true" id="item_neo_6" data-era="zone-neolitico">
            <svg viewBox="0 0 100 100">
                <rect x="10" y="50" width="35" height="35" fill="#E0E0E0" stroke="#9E9E9E" stroke-width="2"/>
                <line x1="10" y1="60" x2="45" y2="60" stroke="#9E9E9E" stroke-width="1.5"/>
                <line x1="10" y1="70" x2="45" y2="70" stroke="#9E9E9E" stroke-width="1.5"/>
                <line x1="10" y1="80" x2="45" y2="80" stroke="#9E9E9E" stroke-width="1.5"/>
                <line x1="20" y1="50" x2="20" y2="85" stroke="#9E9E9E" stroke-width="1.5" stroke-dasharray="10 10"/>
                <line x1="35" y1="55" x2="35" y2="85" stroke="#9E9E9E" stroke-width="1.5" stroke-dasharray="10 10"/>
                <rect x="22" y="65" width="10" height="20" fill="#795548"/>
                <path d="M5 50 L50 50 L50 45 L5 45 Z" fill="#8D6E63"/>

                <rect x="48" y="40" width="45" height="45" fill="#E0E0E0" stroke="#9E9E9E" stroke-width="2"/>
                <line x1="48" y1="50" x2="93" y2="50" stroke="#9E9E9E" stroke-width="1.5"/>
                <line x1="48" y1="60" x2="93" y2="60" stroke="#9E9E9E" stroke-width="1.5"/>
                <line x1="48" y1="70" x2="93" y2="70" stroke="#9E9E9E" stroke-width="1.5"/>
                <line x1="48" y1="80" x2="93" y2="80" stroke="#9E9E9E" stroke-width="1.5"/>
                <line x1="60" y1="40" x2="60" y2="85" stroke="#9E9E9E" stroke-width="1.5" stroke-dasharray="10 10"/>
                <line x1="75" y1="45" x2="75" y2="85" stroke="#9E9E9E" stroke-width="1.5" stroke-dasharray="10 10"/>
                <rect x="65" y="65" width="12" height="20" fill="#5D4037"/>
                <path d="M43 40 L98 40 L98 35 L43 35 Z" fill="#8D6E63"/>
            </svg>
            <span>Villaggio in mattoni</span>
        </div>
        
    </div>

    <!-- Injectiamo i dati Python in Javascript tramite JSON -->
    <script id="curiosita-data" type="application/json">
        /*CURIOSITA_JSON_PLACEHOLDER*/
    </script>

    <script>
        // Leggiamo i dati dal tag script iniettato da Python
        const rawData = document.getElementById('curiosita-data').textContent;
        const curiositaData = JSON.parse(rawData);

        const draggables = document.querySelectorAll('.draggable-item');
        const dropZones = document.querySelectorAll('.drop-zone');
        const pool = document.getElementById('items-pool');
        const modal = document.getElementById('info-modal');
        const modalText = document.getElementById('modal-text');

        function closeModal() {
            modal.style.display = "none";
        }

        // Se clicchi fuori dal modal si chiude
        window.onclick = function(event) {
            if (event.target == modal) {
                closeModal();
            }
        }

        // Aggiungiamo gli eventi a tutti gli oggetti trascinabili
        draggables.forEach(draggable => {
            draggable.addEventListener('dragstart', () => {
                draggable.classList.add('dragging');
                // Salviamo l'id dell'oggetto che stiamo trascinando
                event.dataTransfer.setData('text/plain', draggable.id);
            });

            draggable.addEventListener('dragend', () => {
                draggable.classList.remove('dragging');
            });
            
            // Aggiungiamo il click per il popup (funzionerà solo quando l'oggetto è in zona corretta)
            draggable.addEventListener('click', () => {
                // Se l'oggetto non è più nel div iniziale (pool) ma in una drop zone
                if (draggable.parentElement.classList.contains('drop-zone')) {
                    // Prendi il testo associato al suo ID dal dizionario Python
                    const testo = curiositaData[draggable.id];
                    modalText.innerText = testo;
                    modal.style.display = "flex";
                }
            });
        });

        // Aggiungiamo gli eventi alle zone di destinazione (Paleolitico / Neolitico)
        dropZones.forEach(zone => {
            zone.addEventListener('dragover', e => {
                e.preventDefault(); // Necessario per permettere il drop
                zone.classList.add('dragover');
            });

            zone.addEventListener('dragleave', () => {
                zone.classList.remove('dragover');
            });

            zone.addEventListener('drop', e => {
                e.preventDefault();
                zone.classList.remove('dragover');
                
                const id = event.dataTransfer.getData('text/plain');
                const draggableElement = document.getElementById(id);
                
                // CONTROLLO LA RISPOSTA!
                if (draggableElement.dataset.era === zone.id) {
                    // Risposta Esatta!
                    draggableElement.setAttribute('draggable', 'false'); // Non si muove più
                    zone.appendChild(draggableElement);
                    
                    // Controlla se abbiamo finito
                    if(pool.children.length === 0) {
                        setTimeout(() => alert("Bravissimo! Hai completato la verifica! Riguarda tutte le curiosità! 🎉"), 500);
                    }
                } else {
                    // Risposta Sbagliata!
                    draggableElement.style.borderColor = "red";
                    draggableElement.style.transform = "translateX(10px)";
                    setTimeout(() => {
                        draggableElement.style.borderColor = "#ddd";
                        draggableElement.style.transform = "none";
                    }, 500);
                }
            });
        });
    </script>
</body>
</html>
"""

# Convertiamo il dizionario Python in una stringa JSON
json_curiosita = json.dumps(testi_curiosita)

# Sostituiamo il segnaposto nell'HTML con i dati JSON reali
html_with_data = custom_html.replace('/*CURIOSITA_JSON_PLACEHOLDER*/', json_curiosita)

# Inietta l'HTML dentro Streamlit
# Height 1200 GARANTISCE che ci sia tantissimo spazio in verticale per tutti gli oggetti!
components.html(html_with_data, height=1200, scrolling=False)

st.markdown("---")
st.markdown("*Clicca sugli oggetti una volta posizionati correttamente per scoprire le curiosità!*")
