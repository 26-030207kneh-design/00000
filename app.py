import random
import streamlit as st

st.set_page_config(
    page_title="AI 판사: 균형의 법정 v12.2",
    page_icon="⚖️",
    layout="wide"
)

# ---------------------------------------------------------
# 판사 사법 성향 진단 로직
# ---------------------------------------------------------
def analyze_judge_persona(humanity, law, public, trust):
    if law >= 65 and humanity < 45:
        return {
            "title": "⚖️ 엄격한 법치주의 원칙관",
            "desc": "법조문과 객관적 증거를 철저히 존중하며 엄벌을 통해 법의 엄정함을 세우는 스타일입니다."
        }
    elif humanity >= 65 and law < 45:
        return {
            "title": "❤️ 온건한 인권 중심 재판관",
            "desc": "피고인의 성장 환경, 교화 가능성, 심신 상태를 깊이 참작하는 스타일입니다."
        }
    elif public >= 65 and trust >= 65:
        return {
            "title": "🛡️ 사회 안전 및 공익 수호관",
            "desc": "공공의 안전과 법질서 유지, 사회적 신뢰 회복을 최우선으로 고려하는 스타일입니다."
        }
    else:
        return {
            "title": "⚖️ 균형 잡힌 중용의 사법관",
            "desc": "법적 엄격함과 피고인의 사정, 공공의 이익을 다각도로 양립시키는 성숙한 재판 스타일입니다."
        }

# ---------------------------------------------------------
# 무죄 및 유죄 판례 통합 데이터베이스
# ---------------------------------------------------------
ALL_CASES = [
    {
        "id": "c_innocent1",
        "title": "치과의사 모녀 살인 사건",
        "category": "실제 판례 / 간접증거와 무죄추정",
        "story": "출근한 치과의사 남편이 집을 나선 후 아내와 딸이 안방 욕조에서 숨진 채 발견되었습니다. 사망 시각 추정을 두고 남편의 출근 전인지 후인지가 최대 쟁점이 되었습니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "시신의 수온 변화와 용의자의 동선을 종합할 때 출근 전 살해가 명백하므로 사형에 처해야 합니다.",
        "defense": "사망 시각 추정의 법의학적 오차가 크며, 직접 증거가 전혀 없는 상황에서 정황만으로 처벌할 수 없습니다.",
        "ev2": "[법의학 정밀 재검증] 욕조 물의 식는 속도 및 시신 현상에 관한 학설이 갈려 정확한 사망 시각 특정이 불가능함이 확인됨.",
        "real_verdict": "무죄 확정 (대법원)",
        "real_reason": "대법원은 '의심스러울 때는 피고인의 이익으로'라는 형사재판의 대원칙에 따라, 사망 시각에 대한 간접증거만으로는 합리적 의심을 배척할 만큼 범죄가 입증되지 않았다고 보아 무죄를 확정했습니다.",
        "choices": [
            {"label": "증거불충분으로 무죄 선고", "effects": {"humanity": 10, "law": 15, "public": -5, "trust": 10}},
            {"label": "정황증거 인정으로 사형 선고 (유죄)", "effects": {"humanity": -15, "law": -15, "public": 10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 사망시각 불특정에 따른 무죄 확정", "effects": {"humanity": 10, "law": 15, "public": -5, "trust": 15}},
            {"label": "⚖️ [보강판결] 정황증거 종합 인정으로 무기징역 선고", "effects": {"humanity": -10, "law": -10, "public": 5, "trust": -5}}
        ]
    },
    {
        "id": "c_innocent2",
        "title": "낙동강 변 자갈타이어 살인 사건",
        "category": "실제 판례 / 고문 자백과 재심 무죄",
        "story": "낙동강 변에서 발생한 살인 사건으로 피의자들이 체포되어 자백했으나, 21년 뒤 고문에 의한 허위 자백이었음이 밝혀져 재심이 청구되었습니다.",
        "img1": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80",
        "prosecution": "당시 수사 기록과 자백 진술이 구체적이므로 기존 유죄 판결이 유지되어야 합니다.",
        "defense": "당시 경찰관들의 불법 체포 및 가혹행위(물고문)로 인한 허위 자백이었으므로 무죄입니다.",
        "ev2": "[재심 진실화해위 조사] 당시 경찰관들의 불법 감금 및 물고문 등 가혹행위 정황과 관련 증언이 공식 확인됨.",
        "real_verdict": "재심 무죄 확정 (대법원)",
        "real_reason": "대법원은 불법 수사 및 고문으로 얻은 자백은 증거능력이 없으며, 고문으로 만든 자백 외에 범행을 입증할 증거가 없으므로 무죄를 선고했습니다.",
        "choices": [
            {"label": "위법수사 수집증거 배제 및 무죄 선고", "effects": {"humanity": 15, "law": 15, "public": 5, "trust": 20}},
            {"label": "기존 자백 효력 인정 및 무기징역 유지", "effects": {"humanity": -20, "law": -20, "public": -10, "trust": -25}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 불법고문 인정 및 피고인 전원 무죄 선고", "effects": {"humanity": 15, "law": 20, "public": 5, "trust": 20}},
            {"label": "⚖️ [보강판결] 증거 능력 일부 인정 및 감형 선고", "effects": {"humanity": -10, "law": -10, "public": -5, "trust": -15}}
        ]
    },
    {
        "id": "c1",
        "title": "고유정 전 남편 살인 사건",
        "category": "실제 판례 / 약물 이용 계획 살인",
        "story": "피고인은 전 남편에게 졸피뎀을 투여한 후 살해하고 사체를 훼손·유기한 혐의로 기소되었습니다. 피고인은 성폭행 시도에 대응한 우발적 정당방위라고 주장합니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "치밀하게 계획된 범행이며 범행 수법이 극도로 잔혹하므로 무기징역 선고가 필요합니다.",
        "defense": "우발적인 정당방위였으며, 사체 유기 장소의 직접 증거가 부족합니다.",
        "ev2": "[국과수 정밀 감정] 피고인의 자택 및 차량에서 피해자의 DNA와 함께 계획적 졸피뎀 구입 검색 기록이 확보되었습니다.",
        "real_verdict": "무기징역 확정 (대법원)",
        "real_reason": "대법원은 졸피뎀 사전 구입 및 검색 기록을 바탕으로 우발적 정당방위를 배척하고 치밀한 계획 살인으로 인정하여 무기징역을 확정했습니다.",
        "choices": [
            {"label": "무기징역 선고 (유죄)", "effects": {"humanity": -5, "law": 15, "public": 10, "trust": 10}},
            {"label": "증거불충분 및 정당방위 인정 (무죄)", "effects": {"humanity": 10, "law": -15, "public": -15, "trust": -10}},
            {"label": "징역 20년 감형 선고", "effects": {"humanity": 5, "law": 2, "public": -5, "trust": -2}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 치밀한 계획살인 입증으로 무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 12, "trust": 15}},
            {"label": "⚖️ [보강판결] 범행의 잔혹성 및 사체유기 중벌로 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 15, "trust": 10}}
        ]
    }
]

def clamp(v):
    return max(0, min(100, v))

# 세션 초기화
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.judge_name = "전자고사법관"
    st.session_state.humanity = 50
    st.session_state.law = 50
    st.session_state.public = 50
    st.session_state.trust = 60
    st.session_state.case_index = 0
    st.session_state.postpone_credits = 1  # 💡 한 게임 당 1회 제한
    st.session_state.is_postponed = False
    st.session_state.history = []

    st.session_state.cases = random.sample(ALL_CASES, min(3, len(ALL_CASES)))

st.title("⚖️ AI 판사: 균형의 법정 v12.2")

# 사이드바
with st.sidebar:
    st.header(f"🏛️ {st.session_state.judge_name}")
    st.divider()
    st.subheader("📊 현재 사법 지표")
    st.progress(st.session_state.humanity / 100, text=f"❤️ 인간 중심: {st.session_state.humanity}")
    st.progress(st.session_state.law / 100, text=f"📜 법적 엄격함: {st.session_state.law}")
    st.progress(st.session_state.public / 100, text=f"🏛️ 공공 이익: {st.session_state.public}")
    st.progress(st.session_state.trust / 100, text=f"🛡️ 사회적 신뢰: {st.session_state.trust}")
    st.divider()
    st.info(f"🔍 2차 정밀 증거 요청 찬스: **{st.session_state.postpone_credits} / 1회 남음**")
    st.divider()
    if st.button("🔄 새 게임 시작"):
        st.session_state.clear()
        st.rerun()

# 게임 진행
if st.session_state.case_index < len(st.session_state.cases):
    case = st.session_state.cases[st.session_state.case_index]
    
    st.caption(f"📍 재판 진행도: {st.session_state.case_index + 1} / 3")
    st.subheader(f"⚖️ 사건 {st.session_state.case_index + 1}: {case['title']}")
    st.caption(f"분야: {case['category']}")

    col_img, col_info = st.columns([1, 1.2])
    with col_img:
        if not st.session_state.is_postponed:
            st.image(case["img1"], caption="📸 1차 제출 현장 증거 사진", use_container_width=True)
        else:
            st.image(case["img2"], caption="🔍 2차 정밀 포렌식/부검 증거 사진", use_container_width=True)

    with col_info:
        st.info(f"**사건 개요:**\n\n{case['story']}")
        t1, t2 = st.tabs(["⚖️ 검찰 구형", "🛡️ 변호인 변론"])
        with t1:
            st.write(case["prosecution"])
        with t2:
            st.write(case["defense"])

    if st.session_state.is_postponed:
        st.success(f"🔍 **2차 추가 증거 개시:**\n\n{case['ev2']}")

    st.divider()
    st.subheader("⚖️ 판결 선택")

    if not st.session_state.is_postponed:
        if st.session_state.postpone_credits > 0:
            if st.button("🔍 판결 유예 및 2차 정밀 증거 요청 (게임 당 1회 제한)", key=f"postpone_{st.session_state.case_index}"):
                st.session_state.postpone_credits -= 1
                st.session_state.is_postponed = True
                st.rerun()
        else:
            st.caption("⚠️ *이번 게임의 2차 정밀 증거 요청 찬스를 이미 사용하셨습니다.*")

        st.write("")
        for idx, choice in enumerate(case["choices"]):
            with st.container(border=True):
                st.markdown(f"**{choice['label']}**")
                if st.button("⚖️ 이 판결 선고", key=f"btn_{st.session_state.case_index}_{idx}"):
                    for k, v in choice["effects"].items():
                        st.session_state[k] = clamp(st.session_state[k] + v)
                    
                    st.session_state.history.append({
                        "case": case["title"],
                        "my_decision": choice["label"],
                        "real_verdict": case["real_verdict"],
                        "real_reason": case["real_reason"]
                    })
                    st.session_state.case_index += 1
                    st.session_state.is_postponed = False
                    st.rerun()

    else:
        for idx, choice in enumerate(case["post_choices"]):
            with st.container(border=True):
                st.markdown(f"**{choice['label']}**")
                if st.button("⚖️ 이 보강 판결 선고", key=f"btn_post_{st.session_state.case_index}_{idx}"):
                    for k, v in choice["effects"].items():
                        st.session_state[k] = clamp(st.session_state[k] + v)
                    
                    st.session_state.history.append({
                        "case": f"{case['title']} (2차 증거 제출)",
                        "my_decision": choice["label"],
                        "real_verdict": case["real_verdict"],
                        "real_reason": case["real_reason"]
                    })
                    st.session_state.case_index += 1
                    st.session_state.is_postponed = False
                    st.rerun()

# 종결 화면
else:
    st.balloons()
    st.title("🏛️ 재판 종결: 판사 성향 및 판례 비교 리포트")
    
    persona = analyze_judge_persona(
        st.session_state.humanity,
        st.session_state.law,
        st.session_state.public,
        st.session_state.trust
    )
    
    st.container(border=True).markdown(f"""
    ## 🧐 {st.session_state.judge_name}님의 사법 성향 진단
    ### **{persona['title']}**
    
    {persona['desc']}
    """)

    st.divider()
    st.subheader("📜 내 판결 VS 실제 대법원 판례 비교")
    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"사건 {idx+1}: {item['case']}", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.warning(f"**내 판결:** {item['my_decision']}")
            with col_b:
                st.success(f"**실제 대법원:** {item['real_verdict']}")
            st.caption(f"**판단 이유:** {item['real_reason']}")

    if st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()
