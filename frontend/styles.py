import streamlit as st


def load_css():
    st.html(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">

        <!-- 5-Layer Premium Animated Background -->
        <div class="global-bg-container">
            <!-- Layer 1: Moving Gradient Mesh (handled by .stApp base) -->

            <!-- Layer 2: Floating Green Glow Orbs -->
            <div class="bg-layer orbs">
                <div class="orb orb-1"></div>
                <div class="orb orb-2"></div>
                <div class="orb orb-3"></div>
            </div>

            <!-- Layer 3: AI Neural Network -->
            <div class="bg-layer neural"></div>

            <!-- Layer 4: Agriculture Theme (Floating Leaves) -->
            <div class="bg-layer nature">
                <i class="fa-solid fa-leaf float-leaf l1"></i>
                <i class="fa-solid fa-leaf float-leaf l2"></i>
                <i class="fa-solid fa-leaf float-leaf l3"></i>
                <i class="fa-solid fa-leaf float-leaf l4"></i>
                <i class="fa-solid fa-seedling float-leaf l5"></i>
            </div>

            <!-- Layer 5: Glass Overlay -->
            <div class="bg-layer overlay"></div>
        </div>

        <style>
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css');
        :root{
            --leaf-bg: #020617;
            --leaf-panel: rgba(15, 23, 42, 0.6);
            --leaf-panel-strong: rgba(15, 23, 42, 0.9);
            --leaf-border: rgba(34, 197, 94, 0.2);
            --leaf-primary: #22c55e;
            --leaf-primary-dark: #10b981;
            --leaf-accent: #34d399;
            --leaf-text: #f8fafc;
            --leaf-muted: #94a3b8;
            --leaf-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);

            /* Typography System */
            --h1-size: 72px;
            --h2-size: 48px;
            --h3-size: 32px;
            --body-size: 18px;
        }

        /* Responsive Typography Breakpoints */
        @media (max-width: 1024px) {
            :root {
                --h1-size: 56px;
                --h2-size: 40px;
                --h3-size: 28px;
            }
        }
        @media (max-width: 768px) {
            :root {
                --h1-size: 36px;
                --h2-size: 28px;
                --h3-size: 22px;
                --body-size: 16px;
            }
        }

        /* Enable smooth scrolling for anchor links */
        html, body, .stApp {
            scroll-behavior: smooth;
            font-size: var(--body-size);
            overflow-x: hidden;
        }

        /* Nuke all default HTML/Body spacing */
        html, body {
            margin: 0 !important;
            padding: 0 !important;
        }

        /* --- Hide Streamlit Branding & Chrome Completely --- */
        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"],
        .stBottom {
            display: none !important;
            height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        #MainMenu,
        footer,
        header,
        .stApp > header,
        [data-testid="stToolbar"],
        [data-testid="stDeployButton"],
        [data-testid="manage-app-button"],
        [data-testid="stFooter"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="stHeader"],
        [data-testid="stAppHeader"],
        [data-testid="stSidebarCollapsedControl"],
        [class^="viewerBadge_"],
        [class*="viewerBadge"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }

        /* --- Global 5-Layer Background CSS --- */
        .global-bg-container {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }
        .bg-layer {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            width: 100%; height: 100%;
        }

        /* Layer 2: Floating Orbs */
        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(100px);
            opacity: 0.4;
            animation: floatOrb 20s infinite ease-in-out alternate;
        }
        .orb-1 { width: 40vw; height: 40vw; background: #22c55e; top: -10%; left: -10%; animation-delay: 0s; }
        .orb-2 { width: 35vw; height: 35vw; background: #10b981; bottom: -10%; right: -5%; animation-delay: -5s; }
        .orb-3 { width: 25vw; height: 25vw; background: #34d399; top: 40%; left: 60%; animation-delay: -10s; opacity: 0.2; }

        @keyframes floatOrb {
            0% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(5%, 10%) scale(1.1); }
            100% { transform: translate(-5%, 5%) scale(0.9); }
        }

        /* Layer 3: Neural Network Pattern */
        .bg-layer.neural {
            background-image: radial-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                              radial-gradient(rgba(255,255,255,0.1) 1px, transparent 1px);
            background-position: 0 0, 25px 25px;
            background-size: 50px 50px;
            opacity: 0.15;
            animation: panNetwork 60s linear infinite;
        }
        @keyframes panNetwork {
            from { background-position: 0 0, 25px 25px; }
            to { background-position: 500px 500px, 525px 525px; }
        }

        /* Layer 4: Floating Agriculture Elements */
        .float-leaf {
            position: absolute;
            color: rgba(34, 197, 94, 0.08);
            animation: floatUp 25s linear infinite;
        }
        .l1 { left: 15%; font-size: 40px; animation-duration: 20s; animation-delay: 0s; }
        .l2 { left: 45%; font-size: 24px; animation-duration: 28s; animation-delay: -10s; }
        .l3 { left: 80%; font-size: 55px; animation-duration: 35s; animation-delay: -5s; }
        .l4 { left: 25%; font-size: 30px; animation-duration: 22s; animation-delay: -15s; }
        .l5 { left: 65%; font-size: 45px; animation-duration: 30s; animation-delay: -20s; }

        @keyframes floatUp {
            0% { bottom: -10%; transform: translateX(0) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { bottom: 110%; transform: translateX(100px) rotate(360deg); opacity: 0; }
        }

        /* Layer 5: Glass Overlay */
        .bg-layer.overlay {
            backdrop-filter: blur(60px);
            -webkit-backdrop-filter: blur(60px);
            background: rgba(2, 6, 23, 0.4);
        }

        /* Animated Background */
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stApp {
            background: linear-gradient(135deg, #020617, #0f172a, #064e3b, #022c22);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            color: var(--leaf-text);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        main, section.main, section[data-testid="stMain"] {
            flex: 1;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        [data-testid="stAppViewContainer"] {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        @keyframes contentFadeIn {
            from { opacity: 0; top: 12px; }
            to { opacity: 1; top: 0px; }
        }

        .block-container {
            position: relative;
            z-index: 1;
            animation: contentFadeIn 0.4s ease-out forwards;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        .main .block-container {
            padding-bottom: 0 !important;
        }

        [data-testid="stVerticalBlock"] > div:last-child {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        h1,h2,h3{
            color:var(--leaf-text);
            letter-spacing:0;
            font-family: 'Poppins', sans-serif;
        }

        h1 { font-size: var(--h1-size) !important; line-height: 1.1; }
        h2 { font-size: var(--h2-size) !important; line-height: 1.2; }
        h3 { font-size: var(--h3-size) !important; line-height: 1.3; }

        /* Streamlit main block container constraints */
        .block-container,
        [data-testid="stAppViewBlockContainer"],
        .stMainBlockContainer {
            max-width: 1400px !important;
            padding-top: 110px !important; /* Adjusted for the fixed navbar */
            padding-bottom: 0 !important;
            margin-bottom: 0 !important;
        }

        /* --- Text Selection Styling --- */
        ::selection {
            background-color: rgba(16, 185, 129, 0.4);
            color: var(--leaf-text);
        }
        ::-moz-selection {
            background-color: rgba(16, 185, 129, 0.4);
            color: var(--leaf-text);
        }

        /* Placeholder styling */
        .empty-placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            background: var(--leaf-panel);
            border: 2px dashed var(--leaf-border);
            border-radius: 16px;
            text-align: center;
            color: var(--leaf-muted);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            margin-top: 10px;
        }
        .empty-placeholder i {
            font-size: 48px;
            color: var(--leaf-primary);
            margin-bottom: 16px;
            opacity: 0.8;
        }
        .empty-placeholder h4 {
            color: var(--leaf-text);
            margin-bottom: 8px;
            margin-top: 0;
        }
        .empty-placeholder p {
            margin: 0;
            font-size: 15px;
        }

        /* --- Image Preview Styling --- */
        div[data-testid="stImage"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--leaf-border);
            background: rgba(255, 255, 255, 0.02);
            padding: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        div[data-testid="stImage"] img {
            max-height: 350px !important;
            object-fit: contain !important;
            border-radius: 8px;
        }

        div[data-testid="stImageCaption"] {
            color: var(--leaf-accent);
            font-weight: 600;
            margin-top: 8px;
            font-size: 14px;
        }

        /* --- Modern Glassmorphism Cards --- */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            box-shadow: var(--leaf-shadow);
            transition: all 0.3s ease;
        }
        .glass-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(34, 197, 94, 0.15);
            border-color: rgba(34, 197, 94, 0.3);
        }

        /* --- Modern Tabs Customization --- */
        div[data-testid="stTabs"] {
            margin-top: 16px;
        }

        /* Tab List Container */
        div[data-baseweb="tab-list"] {
            background: rgba(15, 23, 42, 0.4);
            border-radius: 16px;
            padding: 6px;
            gap: 8px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }

        /* Individual Tab Buttons */
        button[data-baseweb="tab"] {
            background: transparent !important;
            border: none !important;
            border-radius: 12px !important;
            color: var(--leaf-muted) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 10px 20px !important;
            transition: all 0.3s ease !important;
        }

        /* Hover State for Tabs */
        button[data-baseweb="tab"]:hover {
            color: var(--leaf-text) !important;
            background: rgba(255, 255, 255, 0.05) !important;
        }

        /* Active Tab State */
        button[data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark)) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
        }

        /* Hide the native active tab highlight bar and border */
        div[data-baseweb="tab-highlight"],
        div[data-baseweb="tab-border"] {
            display: none !important;
        }

        /* Tab Panel Content Spacing */
        div[data-baseweb="tab-panel"] {
            padding-top: 24px !important;
        }

        /* --- Premium Hero Section --- */
        .saas-hero-wrapper {
            position: relative;
            min-height: 90vh;
            display: flex;
            align-items: center;
            padding: 40px 10px;
            margin-bottom: 40px;
            overflow: visible;
        }

        .saas-hero-grid {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 40px;
            align-items: center;
            z-index: 2;
            position: relative;
            width: 100%;
        }

        /* --- Left Content --- */
        .hero-logo {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            color: var(--leaf-primary);
            background: rgba(34, 197, 94, 0.1);
            padding: 10px 20px;
            border-radius: 999px;
            margin-bottom: 32px;
            border: 1px solid rgba(34, 197, 94, 0.25);
            font-family: 'Poppins', sans-serif;
        }

        .hero-title-main {
            font-family: 'Poppins', sans-serif;
            font-size: var(--h1-size);
            font-weight: 800;
            margin: 0;
            background: linear-gradient(135deg, #ffffff 30%, var(--leaf-primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.1;
            margin-bottom: 20px;
        }

        .hero-subtitle-main {
            font-size: var(--body-size);
            color: var(--leaf-muted);
            max-width: 600px;
            margin-bottom: 40px;
            line-height: 1.6;
        }

        .hero-cta-group {
            display: flex;
            gap: 16px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }

        .hero-btn-primary, .hero-btn-secondary {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            padding: 16px 32px;
            border-radius: 99px;
            font-size: 16px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            border: none;
        }

        .hero-btn-primary {
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark));
            color: #020617;
            box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);
        }
        .hero-btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(34, 197, 94, 0.4);
        }

        .hero-btn-secondary {
            background: rgba(255, 255, 255, 0.03);
            color: var(--leaf-text);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        .hero-btn-secondary:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-3px);
        }

        .hero-trust {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            font-size: 14px;
            color: var(--leaf-muted);
            font-weight: 500;
            margin-bottom: 48px;
        }
        .hero-trust i {
            color: var(--leaf-primary);
            margin-right: 6px;
        }

        .hero-stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            max-width: 500px;
        }

        .stat-glass-card {
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: all 0.3s ease;
        }
        .stat-glass-card:hover {
            transform: translateY(-5px);
            border-color: rgba(34, 197, 94, 0.3);
            background: rgba(15, 23, 42, 0.7);
        }
        .hero-stat-val {
            font-size: 32px;
            font-weight: 800;
            color: var(--leaf-text);
            line-height: 1;
            margin-bottom: 8px;
            font-family: 'Poppins', sans-serif;
        }
        .hero-stat-label {
            font-size: 13px;
            color: var(--leaf-accent);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }

        /* --- Right Content: Mock AI Dashboard --- */
        .mock-dashboard {
            background: rgba(15, 23, 42, 0.45);
            border: 1px solid rgba(34, 197, 94, 0.2);
            border-radius: 24px;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            padding: 24px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
            position: relative;
            aspect-ratio: 1;
            display: flex;
            flex-direction: column;
            max-width: 550px;
            margin: 0 auto;
        }

        .mock-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot.red { background: #ef4444; }
        .dot.yellow { background: #eab308; }
        .dot.green { background: #22c55e; }
        .mock-title {
            color: var(--leaf-muted);
            font-size: 14px;
            font-weight: 600;
            margin-left: 8px;
            letter-spacing: 0.5px;
        }

        .mock-body {
            position: relative;
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .scanner-box {
            width: 80%;
            height: 80%;
            border: 2px dashed rgba(34, 197, 94, 0.3);
            border-radius: 20px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }

        .scanner-target {
            font-size: 140px;
            color: rgba(34, 197, 94, 0.9);
            filter: drop-shadow(0 0 24px rgba(34, 197, 94, 0.4));
        }

        @keyframes scan {
            0%, 100% { top: 0%; opacity: 0; }
            10%, 90% { opacity: 1; }
            50% { top: 100%; }
        }

        .laser {
            position: absolute;
            width: 100%;
            height: 3px;
            background: #22c55e;
            box-shadow: 0 0 20px 8px rgba(34, 197, 94, 0.5);
            animation: scan 3.5s ease-in-out infinite;
        }

        /* Floating Result Cards */
        @keyframes floatMock {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-12px); }
        }

        .floating-card {
            position: absolute;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: 16px 20px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            z-index: 10;
            animation: floatMock 6s ease-in-out infinite;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
            min-width: 160px;
        }

        .fc-1 { top: 10%; right: -5%; animation-delay: 0s; border-top: 2px solid #22c55e;}
        .fc-2 { bottom: 25%; left: -5%; animation-delay: 1s; border-left: 2px solid #34d399;}
        .fc-3 { bottom: 5%; right: 0%; animation-delay: 2s; border-bottom: 2px solid #eab308;}

        .fc-title {
            font-size: 12px;
            color: var(--leaf-muted);
            font-weight: 600;
            margin-bottom: 6px;
            text-transform: uppercase;
        }
        .fc-val {
            font-size: 18px;
            font-weight: 800;
            color: var(--leaf-text);
        }
        .text-green { color: #22c55e; }
        .text-accent { color: #34d399; }
        .text-yellow { color: #fbbf24; }
        .text-red { color: #ef4444; }
        .fc-badge {
            display: inline-block;
            background: rgba(234, 179, 8, 0.15);
            color: #eab308;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 700;
        }

        /* --- Responsive Design for Hero --- */
        @media (max-width: 1024px) {
            .saas-hero-grid {
                grid-template-columns: 1.2fr 1fr;
                gap: 30px;
            }
        }

        @media (max-width: 768px) {
            .saas-hero-grid {
                grid-template-columns: 1fr;
                text-align: center;
            }
            .hero-logo { margin: 0 auto 32px; display: inline-flex; }
            .hero-subtitle-main { margin: 0 auto 40px; }
            .hero-cta-group, .hero-trust, .hero-stats-grid {
                justify-content: center;
                margin-left: auto;
                margin-right: auto;
            }
            .mock-dashboard {
                margin-top: 20px;
            }
            .fc-1 { right: 10px; }
            .fc-2 { left: 10px; }
            .fc-3 { right: 10px; }
        }

        @media (max-width: 480px) {
            .saas-hero-wrapper {
                padding: 20px 0;
                min-height: auto;
            }
            .hero-cta-group {
                flex-direction: column;
                width: 100%;
                gap: 12px;
            }
            .hero-btn-primary, .hero-btn-secondary {
                width: 100%;
                justify-content: center;
            }
            .hero-trust {
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }
            .hero-stats-grid {
                grid-template-columns: 1fr;
            }
            .mock-dashboard {
                height: 380px;
                aspect-ratio: auto;
            }
            .scanner-target { font-size: 80px; }
            .floating-card { min-width: 120px; padding: 10px; }
            .fc-val { font-size: 15px; }
        }

        .section-title{
            display:flex;
            align-items:center;
            gap:10px;
            color:var(--leaf-text);
            margin:8px 0 14px;
        }

        .section-title i{
            color:var(--leaf-primary);
        }

        .leaf-panel{
            background:var(--leaf-panel);
            border:1px solid var(--leaf-border);
            border-top: 3px solid var(--leaf-primary);
            border-radius:18px;
            padding:18px;
            margin-bottom:16px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }

        .leaf-panel h2,
        .leaf-panel h3,
        .leaf-panel p,
        .leaf-panel li{
            color:var(--leaf-text);
        }

        .leaf-panel p,
        .leaf-panel li{
            color:var(--leaf-muted);
            font-size:15px;
            line-height:1.55;
        }

        .leaf-panel ul{
            margin-bottom:0;
        }

        div[data-testid="stDataFrame"]{
            border:1px solid var(--leaf-border);
            border-radius:14px;
            overflow:hidden;
        }

        /* File Uploader and Camera Input Styling */
        div[data-testid="stCameraInput"]{
            border-radius:16px;
            border:2px dashed var(--leaf-primary);
            background:rgba(255,255,255,0.04);
            padding:8px;
        }

        section[data-testid="stFileUploader"] {
            background: transparent;
            border: none;
            padding: 0;
        }

        /* Style the internal dropzone to look like a modern upload panel */
        div[data-testid="stFileUploaderDropzone"] {
            border-radius: 16px;
            border: 2px dashed var(--leaf-primary);
            background: rgba(255, 255, 255, 0.04);
            padding: 32px 16px;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        div[data-testid="stFileUploaderDropzone"]:hover {
            background: rgba(82, 183, 136, 0.1);
            border-color: var(--leaf-accent);
        }

        /* Hide Streamlit's default cloud SVG and drag-and-drop text */
        div[data-testid="stFileUploaderDropzone"] svg,
        div[data-testid="stFileUploaderDropzoneInstructions"] {
            display: none;
        }

        /* Inject a custom FontAwesome cloud icon */
        div[data-testid="stFileUploaderDropzone"]::before {
            content: "\\f0ee"; /* fa-cloud-arrow-up */
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 42px;
            color: var(--leaf-primary);
            margin-bottom: 16px;
        }

        /* Make the 'Browse files' button match standard app buttons */
        div[data-testid="stFileUploaderDropzone"] button {
            border: none;
            border-radius: 30px;
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark), var(--leaf-primary));
            background-size: 200% auto;
            color: white;
            font-weight: 700;
            padding: 8px 24px;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        div[data-testid="stFileUploaderDropzone"] button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(82, 183, 136, 0.3);
            background-position: right center;
        }

        div[data-testid="stFileUploaderDropzone"] button:active {
            transform: translateY(1px);
            box-shadow: 0 4px 10px rgba(82, 183, 136, 0.2);
        }

        .stButton button,
        div[data-testid="stDownloadButton"] button {
            border:none;
            border-radius:30px;
            background:linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark), var(--leaf-primary));
            background-size: 200% auto;
            color:white;
            font-weight:700;
            min-height: 48px;
            padding: 12px 24px;
            font-size: 16px;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .stButton button:hover,
        div[data-testid="stDownloadButton"] button:hover {
            transform:translateY(-2px);
            box-shadow:0 12px 28px rgba(16, 185, 129, 0.4);
            background-position: right center;
        }

        .stButton button:active,
        div[data-testid="stDownloadButton"] button:active {
            transform:translateY(1px);
            box-shadow:0 4px 12px rgba(82,183,136,0.2);
        }

        /* --- Dynamic Button Marker System --- */
        .login-btn-marker, .signup-btn-marker, .analyze-btn-marker, .admin-unlock-marker, .admin-lock-marker { display: none; }

        div[data-testid="stElementContainer"]:has(.login-btn-marker),
        div[data-testid="stElementContainer"]:has(.signup-btn-marker),
        div[data-testid="stElementContainer"]:has(.analyze-btn-marker),
        div[data-testid="stElementContainer"]:has(.admin-unlock-marker),
        div[data-testid="stElementContainer"]:has(.admin-lock-marker) {
            display: none !important;
        }

        /* --- Primary Button Base Customization --- */
        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark), var(--leaf-primary));
            background-size: 200% auto;
            color: white !important;
            font-size: 16px;
            font-weight: 700;
            border-radius: 12px !important;
            padding: 14px 24px;
            min-height: 48px;
            border: none;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
            transition: all 0.3s ease;
        }

        div[data-testid="stButton"] button[kind="primary"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(16, 185, 129, 0.45);
            background-position: right center;
        }

        /* --- Analyze Leaf Button (Enlarged & Centered) --- */
        .analyze-btn-spacer { height: 16px; }

        div[data-testid="stElementContainer"]:has(.analyze-btn-marker) + div[data-testid="stElementContainer"] button[kind="primary"] {
            max-width: 320px;
            margin: 0 auto;
            font-size: 18px;
            font-weight: 800;
            padding: 14px 32px;
            min-height: 56px;
            border-radius: 30px !important;
        }

        /* --- Button FontAwesome Icons via Markers --- */
        div[data-testid="stElementContainer"]:has(.analyze-btn-marker) + div[data-testid="stElementContainer"] button[kind="primary"]::before {
            content: "\\f610"; /* fa-microscope */
            font-family: "Font Awesome 6 Free"; font-weight: 900; margin-right: 12px; font-size: 20px;
        }

        div[data-testid="stElementContainer"]:has(.login-btn-marker) + div[data-testid="stElementContainer"] button[kind="primary"]::before {
            content: "\\f2f6"; /* fa-right-to-bracket */
            font-family: "Font Awesome 6 Free"; font-weight: 900; margin-right: 10px; font-size: 18px;
        }

        div[data-testid="stElementContainer"]:has(.signup-btn-marker) + div[data-testid="stElementContainer"] button[kind="primary"]::before {
            content: "\\f234"; /* fa-user-plus */
            font-family: "Font Awesome 6 Free"; font-weight: 900; margin-right: 10px; font-size: 18px;
        }

        div[data-testid="stElementContainer"]:has(.admin-unlock-marker) + div[data-testid="stElementContainer"] button[kind="primary"]::before {
            content: "\\f09c"; /* fa-unlock */
            font-family: "Font Awesome 6 Free"; font-weight: 900; margin-right: 10px; font-size: 18px;
        }

        div[data-testid="stElementContainer"]:has(.admin-lock-marker) + div[data-testid="stElementContainer"] button::before {
            content: "\\f023"; /* fa-lock */
            font-family: "Font Awesome 6 Free"; font-weight: 900; margin-right: 10px; font-size: 16px;
        }

        /* Strip margins from internal p-tags Streamlit adds to prevent uncentering */
        .stButton button p,
        div[data-testid="stDownloadButton"] button p {
            margin: 0;
        }

        /* Add FontAwesome icon to standard download buttons */
        div[data-testid="stDownloadButton"] button::before {
            content: "\\f019";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            margin-right: 8px;
        }

        /* --- Animated Progress Bar Styling (File Uploads & Predictions) --- */
        @keyframes progressFlow {
            0% { background-position: 200% center; }
            100% { background-position: -200% center; }
        }

        div[data-testid="stProgressBar"] > div {
            background-color: rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
        }

        div[data-testid="stProgressBar"] > div > div {
            background: linear-gradient(90deg, var(--leaf-primary-dark), var(--leaf-primary), var(--leaf-accent), var(--leaf-primary), var(--leaf-primary-dark)) !important;
            background-size: 200% auto !important;
            animation: progressFlow 2s linear infinite !important;
            border-radius: 8px !important;
        }

        /* Mobile Responsive adjustments for buttons */
        @media (max-width: 768px) {
            .stButton button,
            div[data-testid="stDownloadButton"] button {
                font-size: 15px;
                padding: 10px 18px;
                min-height: 44px;
            }
        }

        div[data-testid="metric-container"]{
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        div[data-testid="metric-container"]::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, var(--leaf-primary), var(--leaf-accent));
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.4s ease;
        }

        div[data-testid="metric-container"]:hover {
            transform: translateY(-6px);
            border-color: rgba(34, 197, 94, 0.3);
            box-shadow: 0 15px 35px rgba(34, 197, 94, 0.2);
            background: rgba(34, 197, 94, 0.05);
        }

        div[data-testid="metric-container"]:hover::before {
            transform: scaleX(1);
        }

        div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] > * {
            color: var(--leaf-muted) !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        div[data-testid="stMetricValue"] {
            color: var(--leaf-text) !important;
            font-size: 28px !important;
            font-weight: 800 !important;
            font-family: 'Poppins', sans-serif !important;
            transition: color 0.3s ease !important;
        }

        div[data-testid="metric-container"]:hover div[data-testid="stMetricValue"] {
            color: var(--leaf-primary) !important;
        }

        div[data-testid="stExpander"]{
            background:rgba(255,255,255,0.04);
            border:1px solid var(--leaf-border);
            border-radius:14px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        /* --- Beautiful Dialog Styling --- */
        div[data-testid="stModal"] {
            background: rgba(2, 6, 23, 0.1) !important;
            backdrop-filter: blur(4px) !important;
            -webkit-backdrop-filter: blur(4px) !important;
        }

        div[data-testid="stDialog"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(34, 197, 94, 0.04) 40%, rgba(2, 6, 23, 0.6) 100%) !important;
            backdrop-filter: blur(24px) !important;
            -webkit-backdrop-filter: blur(24px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-top-color: rgba(255, 255, 255, 0.25) !important;
            border-left-color: rgba(255, 255, 255, 0.15) !important;
            border-bottom-color: rgba(34, 197, 94, 0.4) !important;
            border-right-color: rgba(34, 197, 94, 0.2) !important;
            border-radius: 24px !important;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
            animation: dialogPop 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) forwards !important;
            transform-origin: center center;
        }
        @keyframes dialogPop {
            0% { transform: scale(0.9); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        button[aria-label="Close"] {
            color: var(--leaf-muted) !important;
            transition: all 0.2s ease !important;
        }
        button[aria-label="Close"]:hover {
            color: #ef4444 !important;
            background: rgba(239, 68, 68, 0.1) !important;
        }

        /* --- Modern Dialog Input Fields --- */
        div[data-testid="stDialog"] div[data-testid="stTextInput"] div[data-baseweb="input"],
        div[data-testid="stDialog"] div[data-testid="stSelectbox"] div[data-baseweb="select"] {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            transition: all 0.3s ease !important;
        }

        div[data-testid="stDialog"] div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
        div[data-testid="stDialog"] div[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
            border-color: var(--leaf-primary) !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
            box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.25) !important;
        }

        div[data-testid="stDialog"] div[data-testid="stTextInput"] input {
            color: var(--leaf-text) !important;
            font-size: 15px !important;
            background-color: transparent !important;
            padding-top: 12px !important;
            padding-bottom: 12px !important;
            caret-color: var(--leaf-primary) !important;
        }

        div[data-testid="stDialog"] div[data-testid="stTextInput"] input::placeholder {
            color: var(--leaf-muted) !important;
            opacity: 0.8 !important;
        }

        /* --- Dialog Thinner Scrollbar --- */
        div[data-testid="stDialog"]::-webkit-scrollbar {
            width: 4px !important;
        }
        div[data-testid="stDialog"]::-webkit-scrollbar-track {
            background: transparent !important;
        }
        div[data-testid="stDialog"]::-webkit-scrollbar-thumb {
            background-color: rgba(255, 255, 255, 0.15) !important;
            border-radius: 10px !important;
            border: none !important;
        }
        div[data-testid="stDialog"]::-webkit-scrollbar-thumb:hover {
            background-color: rgba(255, 255, 255, 0.3) !important;
        }

        /* --- Dialog-Specific Custom Tab Toggle (Pill/Segmented Control) --- */
        div[data-testid="stDialog"] div[data-baseweb="tab-list"] {
            background: rgba(0, 0, 0, 0.4) !important;
            border-radius: 99px !important;
            padding: 6px !important;
            display: flex !important;
            gap: 4px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            margin-bottom: 24px !important;
        }

        div[data-testid="stDialog"] button[data-baseweb="tab"] {
            flex: 1 !important;
            border-radius: 99px !important;
            padding: 12px 16px !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            justify-content: center !important;
        }

        /* --- Dialog Tab Switch Animation --- */
        div[data-testid="stDialog"] div[data-baseweb="tab-panel"] {
            animation: dialogTabSwitch 0.35s cubic-bezier(0.25, 0.8, 0.25, 1) forwards !important;
        }

        @keyframes dialogTabSwitch {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* --- Dialog Buttons Sizing (Smaller & Centered) --- */
        div[data-testid="stDialog"] div[data-testid="stButton"] {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }

        div[data-testid="stDialog"] div[data-testid="stButton"] button {
            min-height: 42px !important;
            height: 42px !important;
            padding: 8px 28px !important;
            font-size: 14.5px !important;
            border-radius: 12px !important;
            width: auto !important;
            min-width: 220px !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }

        div[data-testid="stDialog"] div[data-testid="stButton"] button[kind="primary"]:hover {
            transform: translateY(-3px) scale(1.04) !important;
            box-shadow: 0 12px 28px rgba(34, 197, 94, 0.45) !important;
            background-position: right center !important;
        }

        .chat-shell{
            width: 100%;
            background:rgba(8,28,21,0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border:1px solid rgba(82,183,136,0.35);
            border-radius:18px;
            box-shadow:0 22px 65px rgba(0,0,0,0.45);
            padding:14px;
            box-sizing: border-box;
        }

        /* --- Floating chatbot UI --- */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) {
            position: fixed;
            right: 18px;
            bottom: 80px;
            z-index: 9999;
            width: 56px;
            height: 56px;
            gap: 0 !important;
        }

        .chat-fab-marker {
            display: none;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) button {
            width: 56px !important;
            height: 56px !important;
            min-height: 56px !important;
            border-radius: 999px !important;
            border: 1px solid rgba(82,183,136,0.55) !important;
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-accent), var(--leaf-primary-dark), var(--leaf-primary)) !important;
            background-size: 300% 300% !important;
            box-shadow: var(--leaf-shadow) !important;
            color: white !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            position: relative !important;
            animation: chatFabPulse 2.5s infinite, gradientShift 4s ease infinite !important;
        }

        @keyframes chatFabPulse {
            0% { box-shadow: var(--leaf-shadow), 0 0 0 0 rgba(82, 183, 136, 0.6) !important; }
            70% { box-shadow: var(--leaf-shadow), 0 0 0 20px rgba(82, 183, 136, 0) !important; }
            100% { box-shadow: var(--leaf-shadow), 0 0 0 0 rgba(82, 183, 136, 0) !important; }
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 24px rgba(82,183,136,0.4) !important;
            animation-play-state: paused !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) button p {
            display: none !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-fab-marker) button::after {
            content: "\\f544";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 24px;
            color: white;
            position: absolute !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) {
            position: fixed;
            right: 18px;
            bottom: 150px;
            width: min(420px, calc(100vw - 36px));
            min-width: 320px;
            min-height: 350px;
            max-height: 80vh;
            overflow: auto;
            resize: both;
            z-index: 10000;
            background: rgba(8,28,21,0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(82,183,136,0.35);
            border-radius: 18px;
            box-shadow: var(--leaf-shadow);
            padding: 16px;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stForm"] {
            border: none;
            padding: 0;
        }

        /* --- Chat Panel Action Buttons --- */
        .chat-btn-download-marker, .chat-btn-clear-marker, .chat-btn-close-marker {
            display: none;
        }

    div[data-testid="stElementContainer"]:has(.chat-btn-download-marker),
    div[data-testid="stElementContainer"]:has(.chat-btn-clear-marker),
    div[data-testid="stElementContainer"]:has(.chat-btn-close-marker) {
        display: none !important;
    }

        /* Prevent header columns from stacking on mobile */
        div[data-testid="stHorizontalBlock"]:has(.chat-btn-clear-marker) {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-clear-marker) > div {
            width: auto !important;
            min-width: 0 !important;
            flex: 0 0 auto !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-clear-marker) > div:nth-child(1) {
            flex: 1 1 auto !important;
            width: 100% !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button,
        div[data-testid="stColumn"]:has(.chat-btn-clear-marker) button,
        div[data-testid="stColumn"]:has(.chat-btn-close-marker) button {
            width: 36px !important;
            height: 36px !important;
            min-height: 36px !important;
            position: relative !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 10px !important;
            color: white !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button:hover,
        div[data-testid="stColumn"]:has(.chat-btn-clear-marker) button:hover,
        div[data-testid="stColumn"]:has(.chat-btn-close-marker) button:hover {
            border-color: rgba(82,183,136,0.5) !important;
            background: rgba(82,183,136,0.1) !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button p,
        div[data-testid="stColumn"]:has(.chat-btn-clear-marker) button p,
        div[data-testid="stColumn"]:has(.chat-btn-close-marker) button p,
        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button svg,
        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button::before {
            display: none !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-download-marker) button::after {
            content: "\\f019";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 16px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        div[data-testid="stColumn"]:has(.chat-btn-clear-marker) button::after {
            content: "\\f1f8";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 16px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        div[data-testid="stColumn"]:has(.chat-btn-close-marker) button::after {
            content: "\\f00d";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 18px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        /* --- Instant Send Button (Paper Plane) --- */
        .chat-btn-send-marker {
            display: none;
        }

    div[data-testid="stElementContainer"]:has(.chat-btn-send-marker) {
        display: none !important;
    }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-send-marker) {
            align-items: center !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 8px !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-send-marker) > div {
            width: auto !important;
            min-width: 0 !important;
            flex: 0 0 auto !important;
            padding-bottom: 0 !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-btn-send-marker) > div:nth-child(1) {
            flex: 1 1 auto !important;
            width: 100% !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-send-marker) button {
            width: 42px !important;
            height: 42px !important;
            min-height: 42px !important;
            padding: 0 !important;
            margin: 0 !important;
        display: block !important;
        position: relative !important;
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark)) !important;
            border-radius: 8px !important;
            border: none !important;
        }

    div[data-testid="stColumn"]:has(.chat-btn-send-marker) button * {
            display: none !important;
        }

        div[data-testid="stColumn"]:has(.chat-btn-send-marker) button::after {
            content: "\\f1d8";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            color: white;
            font-size: 16px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        }

        /* Hide Streamlit default form spacing inside panel for nicer look */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) .stTextInput {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) .stTextInput input {
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(82,183,136,0.35) !important;
            color: var(--leaf-text) !important;
            height: 42px !important;
            box-sizing: border-box !important;
            border-radius: 8px !important;
        }


        .chat-card{
            margin-bottom:8px;
        }

        .chat-header{
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:12px;
            margin-bottom:10px;
        }

        .chat-title{
            display:flex;
            align-items:center;
            gap:10px;
            font-weight:800;
            color:white;
        }

        .chat-title i{
            color:var(--leaf-accent);
        }

        .chat-launch-copy{
            margin:0 0 10px;
            color:var(--leaf-muted);
            font-size:13px;
        }

        .chat-log{
            max-height:320px;
            overflow-y:auto;
            padding-right:4px;
            margin-bottom:10px;
        }

        /* --- Native Streamlit Chat Message Bubbles --- */
        .user-msg-marker, .assistant-msg-marker {
            display: none;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] {
            border-radius: 16px;
            padding: 8px 12px;
            margin-bottom: 12px;
            border: 1px solid transparent;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            max-width: 88%;
            width: fit-content;
            overflow-wrap: break-word;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.user-msg-marker) {
            background-color: rgba(82, 183, 136, 0.15) !important;
            border-color: rgba(82, 183, 136, 0.35) !important;
            margin-left: auto !important;
            flex-direction: row-reverse !important;
            border-bottom-right-radius: 4px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.assistant-msg-marker) {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
            margin-right: auto !important;
            border-bottom-left-radius: 4px !important;
        }

        /* --- FontAwesome Chat Avatars --- */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessageAvatar"] {
            background-color: rgba(255,255,255,0.05) !important;
            color: transparent !important; /* Hide original emoji */
            position: relative !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 50% !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessageAvatar"] svg {
            display: none !important; /* Hide Streamlit native SVG if present */
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.user-msg-marker) div[data-testid="stChatMessageAvatar"]::after {
            content: "\\f007"; /* fa-user */
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            color: white;
            font-size: 16px;
            position: absolute;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"]:has(.assistant-msg-marker) div[data-testid="stChatMessageAvatar"]::after {
            content: "\\f544"; /* fa-robot */
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            color: var(--leaf-primary);
            font-size: 16px;
            position: absolute;
        }

        /* --- Chat Table Formatting & Overflow Fix --- */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] table {
            display: block !important;
            overflow-x: auto !important;
            border-collapse: collapse !important;
            margin: 10px 0 !important;
            font-size: 13.5px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] th,
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] td {
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            padding: 6px 12px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) div[data-testid="stChatMessage"] th {
            background: rgba(255, 255, 255, 0.08) !important;
            font-weight: 600 !important;
        }

        .chat-thinking {
            color: var(--leaf-primary);
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 4px 0;
        }

        /* --- Chat Follow-up Suggestions --- */
        .chat-followup-marker { display: none; }

        div[data-testid="stHorizontalBlock"]:has(.chat-followup-marker) {
            gap: 6px !important;
            margin-top: 4px !important;
            margin-bottom: 8px !important;
            flex-wrap: wrap !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-followup-marker) > div[data-testid="stColumn"] {
            width: auto !important;
            min-width: 0 !important;
            flex: 1 1 auto !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-followup-marker) button {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.15) !important;
            color: var(--leaf-muted) !important;
            font-size: 13px !important;
            padding: 6px 12px !important;
            min-height: 0 !important;
            height: auto !important;
            border-radius: 16px !important;
            line-height: 1.3 !important;
            white-space: normal !important;
            text-align: center !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.chat-followup-marker) button:hover {
            border-color: var(--leaf-primary) !important;
            color: var(--leaf-text) !important;
            background: rgba(82,183,136,0.15) !important;
        }

        /* --- Hide SPA Router Bridge --- */
        .hidden-spa-marker { display: none; }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .hidden-spa-marker) {
            position: absolute !important;
            width: 0 !important;
            height: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
            overflow: hidden !important;
        }

        /* --- Global Scrollbar Styling --- */
        ::-webkit-scrollbar {
            width: 14px;
            height: 14px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: var(--leaf-primary-dark);
            border-radius: 10px;
            border: 4px solid transparent;
            background-clip: padding-box;
        }

        ::-webkit-scrollbar-thumb:hover {
            background-color: var(--leaf-primary);
        }

        ::-webkit-scrollbar-corner {
            background: transparent;
        }

        /* Firefox cross-browser support */
        * {
            scrollbar-width: thin;
            scrollbar-color: var(--leaf-primary-dark) rgba(255, 255, 255, 0.02);
        }

        /* --- Global Sidebar Removal --- */
        section[data-testid="stSidebar"],
        button[data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }

        /* --- PREMIUM RESPONSIVE NAVBAR --- */
        .navbar-container-marker { display: none; }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .navbar-container-marker) {
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
            width: 100%;
            background: transparent;
            gap: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            display: block !important;
        }

        :root {
            --nav-height: 72px;
            --nav-x-pad: 40px;
            --nav-gap: 32px;
            --nav-link-fs: 15px;
        }

        .nav-background {
            position: absolute;
            top: 0; left: 0; right: 0;
            height: var(--nav-height);
            background: rgba(2, 8, 23, 0.72);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            z-index: 1;
        }

        .nav-processing-line {
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 2px;
            width: 100%;
            background: linear-gradient(90deg, transparent, #22C55E, #16A34A, transparent);
            background-size: 200% auto;
            animation: navProcessing 3s linear infinite;
            z-index: 15;
            box-shadow: 0 -1px 8px rgba(34, 197, 94, 0.8);
        }
        @keyframes navProcessing {
            0% { background-position: -100% center; }
            100% { background-position: 200% center; }
        }

        .nav-orb {
            position: absolute;
            width: 250px;
            height: 250px;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.15;
            z-index: 2;
            pointer-events: none;
        }
        .nav-orb-left { background: #22C55E; left: -50px; top: calc(-1 * var(--nav-height)); }
        .nav-orb-right { background: #3B82F6; right: -50px; top: calc(-1 * var(--nav-height)); }

        .mobile-menu-toggle { display: none; }

        .nav-container-inner {
            position: relative;
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: space-between;
            max-width: 1440px;
            margin: 0 auto;
            height: var(--nav-height);
            padding-left: var(--nav-x-pad);
            padding-right: calc(var(--nav-x-pad) + 140px);
        }


        .nav-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            white-space: nowrap;
            flex-shrink: 0;
        }

        .brand-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: rgba(34, 197, 94, 0.15);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: #22C55E;
            font-size: 16px;
            box-shadow: 0 0 20px rgba(34, 197, 94, 0.4);
        }

        .nav-right {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 18px;
            min-width: 0;
            flex: 1;
        }

        .nav-links {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: var(--nav-gap);
            flex: 1;
            min-width: 0;
        }

        .nav-link {
            color: rgba(255, 255, 255, 0.72);
            text-decoration: none;
            font-weight: 600;
            font-size: var(--nav-link-fs);
            transition: all 0.25s ease;
            position: relative;
            padding: 6px 0;
            background: transparent !important;
            box-shadow: none !important;
            white-space: nowrap;
        }

        .nav-link:hover,
        .nav-link.active {
            color: #ffffff;
        }

        .nav-link::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 0;
            height: 2px;
            background: #22C55E;
            transition: width 0.25s ease;
            border-radius: 999px;
            transform: translateX(-50%);
        }

        .nav-link:hover::after,
        .nav-link.active::after {
            width: 100%;
        }

        .nav-link-cta {
            margin-top: 4px;
            color: rgba(255,255,255,0.9) !important;
        }

        .hamburger-btn {
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 6px;
            width: 36px;
            height: 36px;
            cursor: pointer;
            z-index: 110;
            user-select: none;
        }

        .hamburger-btn span {
            display: block;
            width: 22px;
            height: 2px;
            background: #ffffff;
            border-radius: 2px;
            transition: all 0.25s ease;
        }

        .nav-btn-marker { display: none; }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .navbar-container-marker)
        > div[data-testid="stElementContainer"]:has(.nav-btn-marker) + div[data-testid="stElementContainer"] {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            /* keep CTA well separated from nav links */
            right: 40px;
            z-index: 20;
            width: auto;
            display: flex;
            align-items: center;
            height: 44px;
            gap: 10px;
        }


        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .navbar-container-marker)
        > div[data-testid="stElementContainer"]:has(.nav-btn-marker) + div[data-testid="stElementContainer"] button {
            background: linear-gradient(135deg, var(--leaf-primary), var(--leaf-primary-dark)) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 14.5px !important;
            padding: 0 22px !important;
            height: 42px !important;
            min-height: 42px !important;
            white-space: nowrap;
            box-shadow: 0 10px 22px rgba(34, 197, 94, 0.22) !important;
            transition: all 0.25s ease !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .navbar-container-marker)
        > div[data-testid="stElementContainer"]:has(.nav-btn-marker) + div[data-testid="stElementContainer"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 16px 32px rgba(34, 197, 94, 0.32) !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .navbar-container-marker)
        > div[data-testid="stElementContainer"]:has(.nav-btn-marker.logged-in) + div[data-testid="stElementContainer"] button {
            background: rgba(239, 68, 68, 0.1) !important;
            color: #ef4444 !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            box-shadow: none !important;
            padding: 0 18px !important;
        }

        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .navbar-container-marker)
        > div[data-testid="stElementContainer"]:has(.nav-btn-marker.logged-in) + div[data-testid="stElementContainer"] button:hover {
            background: rgba(239, 68, 68, 0.15) !important;
        }

        /* Mobile dropdown */
        .mobile-dropdown {
            position: absolute;
            top: var(--nav-height);
            left: 0;
            right: 0;
            background: rgba(2, 8, 23, 0.95);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
            display: flex;
            flex-direction: column;
            padding: 0;
            overflow: hidden;
            z-index: 9;
            transform-origin: top;
            transform: translateY(-6px);
            opacity: 0;
            pointer-events: none;
            transition: transform 0.25s ease, opacity 0.2s ease;
            max-height: 80vh;
        }

        .mobile-nav-links {
            display: flex;
            flex-direction: column;
            padding: 18px;
            gap: 10px;
        }

        .mobile-dropdown .nav-link {
            font-size: 16px;
            font-weight: 650;
            padding: 12px 14px;
            border-radius: 12px;
            color: rgba(255,255,255,0.82);
            display: block;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.2s ease;
        }

        .mobile-dropdown .nav-link:hover,
        .mobile-dropdown .nav-link.active {
            background: rgba(34, 197, 94, 0.10);
            border-color: rgba(34, 197, 94, 0.25);
            color: #22C55E;
        }

        .mobile-dropdown .nav-link::after { display: none; }

        /* Checkbox toggle animations */
        #mobile-menu-toggle:checked ~ .mobile-dropdown {
            transform: translateY(0);
            opacity: 1;
            pointer-events: auto;
        }

        #mobile-menu-toggle:checked ~ .nav-container-inner .hamburger-btn span:nth-child(1) { transform: translateY(8px) rotate(45deg); }
        #mobile-menu-toggle:checked ~ .nav-container-inner .hamburger-btn span:nth-child(2) { opacity: 0; }
        #mobile-menu-toggle:checked ~ .nav-container-inner .hamburger-btn span:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }

        /* Breakpoints (explicit) */
        @media (min-width: 1440px) {
            :root { --nav-x-pad: 56px; --nav-gap: 36px; --nav-link-fs: 15.5px; }
        }

        @media (max-width: 1199px) {
            :root { --nav-x-pad: 28px; --nav-gap: 24px; --nav-link-fs: 14.5px; }
        }

        @media (max-width: 991px) {
            :root { --nav-x-pad: 22px; --nav-gap: 18px; --nav-link-fs: 14px; }
        }

        @media (max-width: 768px) {
            :root { --nav-x-pad: 18px; }
            .nav-links { display: none; }
            .hamburger-btn { display: flex; }
            .nav-container-inner { padding: 0 var(--nav-x-pad); }

            /* hide CTA/user area on closed mobile menu; dropdown takes over */
            div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .navbar-container-marker)
            > div[data-testid="stElementContainer"]:has(.nav-btn-marker),
            div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .navbar-container-marker)
            > div[data-testid="stElementContainer"]:has(.nav-btn-marker) + div[data-testid="stElementContainer"] {
                display: none !important;
            }
        }

        @media (max-width: 576px) {
            :root { --nav-link-fs: 14.5px; }
        }

        @media (max-width: 375px) {
            :root { --nav-gap: 14px; --nav-link-fs: 14px; }
        }


        /* --- Auto-hiding Success Message --- */
        @keyframes autoFadeOut {
            0% { opacity: 1; transform: translateY(0); }
            85% { opacity: 1; transform: translateY(0); }
            100% { opacity: 0; transform: translateY(-10px); }
        }
        .success-msg-anim {
            color: #22c55e;
            font-size: 14px;
            margin-top: 8px;
            font-weight: 600;
            animation: autoFadeOut 3.2s forwards;
            pointer-events: none;
        }

        /* --- Custom Toast Notification --- */
        .custom-toast-container {
            position: fixed;
            bottom: 30px;
            top: 90px;
            right: 30px;
            z-index: 100000;
            animation: toastSlideIn 0.5s cubic-bezier(0.25, 0.8, 0.25, 1) forwards, toastFadeOut 0.5s ease forwards 4.5s;
            pointer-events: none;
        }

        .custom-toast {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-left: 4px solid var(--leaf-primary);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            gap: 16px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(34, 197, 94, 0.1);
        }

        @keyframes toastSlideIn {
            from { transform: translateX(120%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
            from { transform: translateY(-150%); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        @keyframes toastFadeOut {
            from { opacity: 1; transform: translateX(0); }
            to { opacity: 0; transform: translateX(120%); visibility: hidden; }
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(-150%); visibility: hidden; }
        }

        /* --- Enterprise SaaS Footer --- */
        .saas-footer {
            position: relative;
            width: 100vw;
            margin-left: calc(50% - 50vw);
            margin-right: calc(50% - 50vw);
            margin-top: auto;
            margin-bottom: 0 !important;
            padding: 60px 20px 20px;
            background: rgba(10, 15, 28, 0.85);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            overflow: hidden;
            color: var(--leaf-text);
            border-top: 1px solid rgba(255,255,255,0.05);
        }

        /* Gradient Top Border */
        .footer-gradient-line {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--leaf-primary), var(--leaf-accent), transparent);
            background-size: 200% auto;
            animation: footerGradientMove 3s linear infinite;
        }

        @keyframes footerGradientMove {
            0% { background-position: 0% center; }
            100% { background-position: 200% center; }
        }

        /* Floating Particles */
        .footer-particle {
            position: absolute;
            border-radius: 50%;
            background: var(--leaf-primary);
            filter: blur(3px);
            opacity: 0.15;
            animation: footerFloat 12s infinite linear;
            pointer-events: none;
        }
        .fp-1 { width: 10px; height: 10px; top: 80%; left: 10%; }
        .fp-2 { width: 16px; height: 16px; top: 40%; left: 80%; animation-duration: 18s; }
        .fp-3 { width: 6px; height: 6px; top: 20%; left: 40%; animation-duration: 15s; }
        .fp-4 { width: 12px; height: 12px; top: 60%; left: 20%; animation-duration: 20s; }

        @keyframes footerFloat {
            0% { transform: translateY(0) rotate(0deg); opacity: 0; }
            50% { opacity: 0.3; }
            100% { transform: translateY(-120px) rotate(360deg); opacity: 0; }
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }

        /* Stat Bar */
        .footer-stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            padding: 24px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 32px;
            gap: 20px;
        }
        .f-stat { text-align: center; flex: 1; min-width: 120px; }
        .f-stat-val { display: block; font-size: 28px; font-weight: 800; color: var(--leaf-text); font-family: 'Poppins', sans-serif; }
        .f-stat-label { font-size: 13px; color: var(--leaf-primary); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }

        /* Trust Indicators */
        .footer-trust {
            display: flex;
            justify-content: center;
            gap: 24px;
            flex-wrap: wrap;
            margin-bottom: 40px;
            font-size: 14px;
            color: var(--leaf-muted);
            font-weight: 500;
        }
        .footer-trust i { color: var(--leaf-primary); margin-right: 8px; }

        /* Columns Grid */
        .footer-grid {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1.5fr;
            gap: 40px;
            margin-bottom: 48px;
        }

        /* Column Elements */
        .f-logo {
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .f-logo-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            background: rgba(34, 197, 94, 0.15);
            color: var(--leaf-primary);
            border-radius: 8px;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }

        .f-desc {
            color: var(--leaf-muted);
            font-size: 15px;
            line-height: 1.6;
            margin-bottom: 24px;
        }

        .f-badges { display: flex; gap: 12px; flex-wrap: wrap; }
        .f-badge {
            padding: 6px 12px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 99px;
            font-size: 12px;
            font-weight: 600;
            color: var(--leaf-text);
        }
        .nvidia-badge {
            background: rgba(118, 185, 0, 0.1);
            border-color: rgba(118, 185, 0, 0.3);
            color: #76B900;
        }

        .f-heading {
            font-size: 16px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 20px;
            margin-top: 0;
            font-family: 'Poppins', sans-serif;
        }

        .f-link, .f-social {
            display: block;
            color: var(--leaf-muted);
            text-decoration: none;
            font-size: 15px;
            margin-bottom: 12px;
            transition: all 0.2s ease;
        }
        .f-link:hover, .f-social:hover {
            color: var(--leaf-primary);
            transform: translateX(4px);
        }
        .f-social i {
            width: 20px;
            color: var(--leaf-primary);
        }

        /* Newsletter Form */
        .f-form {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 4px;
        }
        .f-input {
            background: transparent;
            border: none;
            color: var(--leaf-text);
            padding: 10px 12px;
            font-size: 14px;
            width: 100%;
            outline: none;
            font-family: 'Inter', sans-serif;
        }
        .f-submit {
            background: var(--leaf-primary);
            color: #000;
            border: none;
            width: 36px;
            height: 36px;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        .f-submit:hover {
            background: var(--leaf-accent);
            transform: scale(1.05);
        }

        /* Bottom Section */
        .footer-bottom {
            padding-top: 24px;
            border-top: 1px solid rgba(255,255,255,0.05);
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--leaf-muted);
            font-size: 14px;
            flex-wrap: wrap;
            gap: 16px;
        }
        .footer-bottom p { margin: 0; }

        /* Responsive Footer */
        @media (max-width: 1024px) {
            .footer-grid { grid-template-columns: 1fr 1fr; }
        }
        @media (max-width: 768px) {
            .footer-grid { grid-template-columns: 1fr; gap: 32px; }
            .footer-bottom { flex-direction: column; text-align: center; }
            .f-link:hover, .f-social:hover { transform: none; }
        }

        @keyframes growBar {
            0% { transform: scaleX(0); }
            100% { transform: scaleX(1); }
        }

        @keyframes popInCard {
            0% { opacity: 0; transform: translateY(10px) scale(0.95); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        .pop-in-card {
            opacity: 0;
            animation: popInCard 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
        }

        @keyframes dashboardSlideUp {
            0% { opacity: 0; transform: translateY(40px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .dashboard-slide-up-marker) {
            opacity: 0;
            animation: dashboardSlideUp 0.8s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
        }
        .dashboard-slide-up-marker { display: none; }

        .staggered-slide-up {
            opacity: 0;
            animation: dashboardSlideUp 0.6s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
        }

        @keyframes chatPanelPop {
            0% { opacity: 0; transform: scale(0.9) translateY(20px); }
            100% { opacity: 1; transform: scale(1) translateY(0); }
        }
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .chat-floating-panel-marker) {
            transform-origin: bottom right;
            animation: chatPanelPop 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
        }
        </style>
        <script>
        const initCounters = () => {
            document.querySelectorAll('.count-up').forEach(el => {
                if(el.dataset.animated) return;
                el.dataset.animated = 'true';
                let target = parseFloat(el.dataset.target);
                let duration = 1000;
                let start = performance.now();
                let update = (t) => {
                    let p = Math.min((t - start) / duration, 1);
                    let ease = 1 - Math.pow(1 - p, 4); // Quartic ease out
                    el.innerText = (ease * target).toFixed(1) + '%';
                    if(p < 1) requestAnimationFrame(update);
                    else el.innerText = target.toFixed(1) + '%';
                };
                requestAnimationFrame(update);
            });
        };

        const initChatDrag = () => {
            const marker = document.querySelector('.chat-floating-panel-marker');
            if (marker) {
                const panel = marker.closest('div[data-testid="stVerticalBlock"]');
                if (panel && !panel.dataset.dragAttached) {
                    panel.dataset.dragAttached = 'true';
                    let isDragging = false;
                    let offsetX, offsetY;

                    panel.addEventListener('mousedown', (e) => {
                        const tag = e.target.tagName.toLowerCase();
                        if (['input', 'button', 'textarea'].includes(tag) || e.target.closest('button')) return;

                        // Prevent drag if clicking the resize handle (bottom-right area)
                        const rect = panel.getBoundingClientRect();
                        if (e.clientX > rect.right - 20 && e.clientY > rect.bottom - 20) return;

                        if (e.detail === 2) {
                            isDragging = true;
                            offsetX = e.clientX - rect.left;
                            offsetY = e.clientY - rect.top;
                            panel.style.cursor = 'grabbing';
                            panel.style.animation = 'none';
                            panel.style.transition = 'none';

                            // Prevent text selection while dragging
                            document.body.style.userSelect = 'none';
                            window.getSelection().removeAllRanges();
                            e.preventDefault();
                        }
                    });

                    document.addEventListener('mousemove', (e) => {
                        if (!isDragging) return;
                        e.preventDefault();
                        panel.style.left = (e.clientX - offsetX) + 'px';
                        panel.style.top = (e.clientY - offsetY) + 'px';
                        panel.style.bottom = 'auto';
                        panel.style.right = 'auto';
                    });

                    document.addEventListener('mouseup', () => {
                        if (isDragging) {
                            isDragging = false;
                            panel.style.cursor = 'auto';
                            // Restore text selection
                            document.body.style.userSelect = '';
                        }
                    });
                }
            }
        };

        const runObservers = () => {
            initCounters();
            initChatDrag();
        };

        // Initial run
        setTimeout(runObservers, 100);
        if (!window.customUiObserver) {
            if (window.counterObserver) { window.counterObserver.disconnect(); }
            window.customUiObserver = new MutationObserver(runObservers);
            window.customUiObserver.observe(document.body, { childList: true, subtree: true });
        }
        </script>
        """
    )
