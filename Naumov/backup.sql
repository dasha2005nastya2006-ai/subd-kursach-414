--
-- PostgreSQL database dump
--

\restrict kGW9TFVQIeO279vjCNQcHyjD1vpGJ9b9iBIfyP8pnxYqwhaiCPdMnCLWWxgwDcI

-- Dumped from database version 14.20 (Ubuntu 14.20-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.20 (Ubuntu 14.20-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: administrator_role; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.administrator_role AS ENUM (
    'admin',
    'manager',
    'auditor'
);


ALTER TYPE public.administrator_role OWNER TO postgres;

--
-- Name: gruppa_zachislenie_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.gruppa_zachislenie_status AS ENUM (
    'active',
    'finished',
    'expelled'
);


ALTER TYPE public.gruppa_zachislenie_status OWNER TO postgres;

--
-- Name: poseshchaemost_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.poseshchaemost_status AS ENUM (
    'present',
    'absent',
    'late'
);


ALTER TYPE public.poseshchaemost_status OWNER TO postgres;

--
-- Name: student_status; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.student_status AS ENUM (
    'active',
    'inactive'
);


ALTER TYPE public.student_status OWNER TO postgres;

--
-- Name: tip_oplaty; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tip_oplaty AS ENUM (
    'nal',
    'karta',
    'online'
);


ALTER TYPE public.tip_oplaty OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: administrator; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.administrator (
    administrator_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash text NOT NULL,
    role public.administrator_role DEFAULT 'manager'::public.administrator_role,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.administrator OWNER TO postgres;

--
-- Name: administrator_administrator_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.administrator_administrator_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.administrator_administrator_id_seq OWNER TO postgres;

--
-- Name: administrator_administrator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.administrator_administrator_id_seq OWNED BY public.administrator.administrator_id;


--
-- Name: auditoriya; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auditoriya (
    auditoriya_id integer NOT NULL,
    nazvanie character varying(50) NOT NULL,
    vmestimost integer,
    CONSTRAINT auditoriya_vmestimost_check CHECK ((vmestimost > 0))
);


ALTER TABLE public.auditoriya OWNER TO postgres;

--
-- Name: auditoriya_auditoriya_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auditoriya_auditoriya_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auditoriya_auditoriya_id_seq OWNER TO postgres;

--
-- Name: auditoriya_auditoriya_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auditoriya_auditoriya_id_seq OWNED BY public.auditoriya.auditoriya_id;


--
-- Name: gruppa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.gruppa (
    gruppa_id integer NOT NULL,
    kurs_id integer,
    prepodavatel_id integer,
    nazvanie character varying(100) NOT NULL,
    data_nachala date NOT NULL,
    max_studentov integer,
    CONSTRAINT gruppa_max_studentov_check CHECK ((max_studentov > 0))
);


ALTER TABLE public.gruppa OWNER TO postgres;

--
-- Name: gruppa_gruppa_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.gruppa_gruppa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gruppa_gruppa_id_seq OWNER TO postgres;

--
-- Name: gruppa_gruppa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.gruppa_gruppa_id_seq OWNED BY public.gruppa.gruppa_id;


--
-- Name: kategoriya_kursov; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kategoriya_kursov (
    kategoriya_id integer NOT NULL,
    nazvanie character varying(100) NOT NULL,
    opisanie text
);


ALTER TABLE public.kategoriya_kursov OWNER TO postgres;

--
-- Name: kategoriya_kursov_kategoriya_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kategoriya_kursov_kategoriya_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kategoriya_kursov_kategoriya_id_seq OWNER TO postgres;

--
-- Name: kategoriya_kursov_kategoriya_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kategoriya_kursov_kategoriya_id_seq OWNED BY public.kategoriya_kursov.kategoriya_id;


--
-- Name: kurs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kurs (
    kurs_id integer NOT NULL,
    kategoriya_id integer,
    nazvanie character varying(100) NOT NULL,
    prodolzhitelnost_chasy integer NOT NULL,
    stoimost_mesyac numeric(10,2) NOT NULL,
    opisanie text
);


ALTER TABLE public.kurs OWNER TO postgres;

--
-- Name: kurs_kurs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kurs_kurs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kurs_kurs_id_seq OWNER TO postgres;

--
-- Name: kurs_kurs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kurs_kurs_id_seq OWNED BY public.kurs.kurs_id;


--
-- Name: oplata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oplata (
    oplata_id integer NOT NULL,
    student_id integer,
    data date DEFAULT CURRENT_DATE,
    summa numeric(12,2) NOT NULL,
    tip_oplaty public.tip_oplaty NOT NULL,
    kommentariy text,
    CONSTRAINT oplata_summa_check CHECK ((summa > (0)::numeric))
);


ALTER TABLE public.oplata OWNER TO postgres;

--
-- Name: oplata_oplata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.oplata_oplata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oplata_oplata_id_seq OWNER TO postgres;

--
-- Name: oplata_oplata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.oplata_oplata_id_seq OWNED BY public.oplata.oplata_id;


--
-- Name: otsenka; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.otsenka (
    otsenka_id integer NOT NULL,
    student_id integer,
    kurs_id integer,
    znachenie integer,
    data date DEFAULT CURRENT_DATE,
    kommentariy text,
    CONSTRAINT otsenka_znachenie_check CHECK (((znachenie >= 1) AND (znachenie <= 100)))
);


ALTER TABLE public.otsenka OWNER TO postgres;

--
-- Name: otsenka_otsenka_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.otsenka_otsenka_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.otsenka_otsenka_id_seq OWNER TO postgres;

--
-- Name: otsenka_otsenka_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.otsenka_otsenka_id_seq OWNED BY public.otsenka.otsenka_id;


--
-- Name: poseshchaemost; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.poseshchaemost (
    poseshchaemost_id integer NOT NULL,
    zanyatie_id integer,
    student_id integer,
    status public.poseshchaemost_status NOT NULL
);


ALTER TABLE public.poseshchaemost OWNER TO postgres;

--
-- Name: poseshchaemost_poseshchaemost_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.poseshchaemost_poseshchaemost_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.poseshchaemost_poseshchaemost_id_seq OWNER TO postgres;

--
-- Name: poseshchaemost_poseshchaemost_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.poseshchaemost_poseshchaemost_id_seq OWNED BY public.poseshchaemost.poseshchaemost_id;


--
-- Name: prepodavatel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prepodavatel (
    prepodavatel_id integer NOT NULL,
    familiya character varying(50) NOT NULL,
    imya character varying(50) NOT NULL,
    telefon character varying(20),
    email character varying(100),
    specializaciya character varying(100),
    data_nachala date NOT NULL
);


ALTER TABLE public.prepodavatel OWNER TO postgres;

--
-- Name: prepodavatel_prepodavatel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.prepodavatel_prepodavatel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.prepodavatel_prepodavatel_id_seq OWNER TO postgres;

--
-- Name: prepodavatel_prepodavatel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.prepodavatel_prepodavatel_id_seq OWNED BY public.prepodavatel.prepodavatel_id;


--
-- Name: roditel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roditel (
    roditel_id integer NOT NULL,
    familiya character varying(50) NOT NULL,
    imya character varying(50) NOT NULL,
    telefon character varying(20),
    email character varying(100),
    rodstvo character varying(30) NOT NULL
);


ALTER TABLE public.roditel OWNER TO postgres;

--
-- Name: roditel_roditel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roditel_roditel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.roditel_roditel_id_seq OWNER TO postgres;

--
-- Name: roditel_roditel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roditel_roditel_id_seq OWNED BY public.roditel.roditel_id;


--
-- Name: roditel_student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roditel_student (
    student_id integer NOT NULL,
    roditel_id integer NOT NULL
);


ALTER TABLE public.roditel_student OWNER TO postgres;

--
-- Name: student; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student (
    student_id integer NOT NULL,
    familiya character varying(50) NOT NULL,
    imya character varying(50) NOT NULL,
    otchestvo character varying(50),
    data_rozhdeniya date NOT NULL,
    telefon character varying(20),
    email character varying(100),
    data_registracii date DEFAULT CURRENT_DATE,
    status public.student_status DEFAULT 'active'::public.student_status
);


ALTER TABLE public.student OWNER TO postgres;

--
-- Name: student_gruppa; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.student_gruppa (
    student_id integer NOT NULL,
    gruppa_id integer NOT NULL,
    data_zachisleniya date DEFAULT CURRENT_DATE,
    status public.gruppa_zachislenie_status DEFAULT 'active'::public.gruppa_zachislenie_status
);


ALTER TABLE public.student_gruppa OWNER TO postgres;

--
-- Name: student_student_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.student_student_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.student_student_id_seq OWNER TO postgres;

--
-- Name: student_student_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.student_student_id_seq OWNED BY public.student.student_id;


--
-- Name: zanyatie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.zanyatie (
    zanyatie_id integer NOT NULL,
    gruppa_id integer,
    data_vremya timestamp without time zone NOT NULL,
    auditoriya_id integer,
    tema_zanyatiya character varying(200)
);


ALTER TABLE public.zanyatie OWNER TO postgres;

--
-- Name: zanyatie_zanyatie_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.zanyatie_zanyatie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.zanyatie_zanyatie_id_seq OWNER TO postgres;

--
-- Name: zanyatie_zanyatie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.zanyatie_zanyatie_id_seq OWNED BY public.zanyatie.zanyatie_id;


--
-- Name: administrator administrator_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrator ALTER COLUMN administrator_id SET DEFAULT nextval('public.administrator_administrator_id_seq'::regclass);


--
-- Name: auditoriya auditoriya_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoriya ALTER COLUMN auditoriya_id SET DEFAULT nextval('public.auditoriya_auditoriya_id_seq'::regclass);


--
-- Name: gruppa gruppa_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gruppa ALTER COLUMN gruppa_id SET DEFAULT nextval('public.gruppa_gruppa_id_seq'::regclass);


--
-- Name: kategoriya_kursov kategoriya_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kategoriya_kursov ALTER COLUMN kategoriya_id SET DEFAULT nextval('public.kategoriya_kursov_kategoriya_id_seq'::regclass);


--
-- Name: kurs kurs_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kurs ALTER COLUMN kurs_id SET DEFAULT nextval('public.kurs_kurs_id_seq'::regclass);


--
-- Name: oplata oplata_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oplata ALTER COLUMN oplata_id SET DEFAULT nextval('public.oplata_oplata_id_seq'::regclass);


--
-- Name: otsenka otsenka_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.otsenka ALTER COLUMN otsenka_id SET DEFAULT nextval('public.otsenka_otsenka_id_seq'::regclass);


--
-- Name: poseshchaemost poseshchaemost_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.poseshchaemost ALTER COLUMN poseshchaemost_id SET DEFAULT nextval('public.poseshchaemost_poseshchaemost_id_seq'::regclass);


--
-- Name: prepodavatel prepodavatel_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prepodavatel ALTER COLUMN prepodavatel_id SET DEFAULT nextval('public.prepodavatel_prepodavatel_id_seq'::regclass);


--
-- Name: roditel roditel_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roditel ALTER COLUMN roditel_id SET DEFAULT nextval('public.roditel_roditel_id_seq'::regclass);


--
-- Name: student student_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student ALTER COLUMN student_id SET DEFAULT nextval('public.student_student_id_seq'::regclass);


--
-- Name: zanyatie zanyatie_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zanyatie ALTER COLUMN zanyatie_id SET DEFAULT nextval('public.zanyatie_zanyatie_id_seq'::regclass);


--
-- Data for Name: administrator; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administrator (administrator_id, username, password_hash, role, created_at) FROM stdin;
\.


--
-- Data for Name: auditoriya; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auditoriya (auditoriya_id, nazvanie, vmestimost) FROM stdin;
1	Аудитория 101	10
2	Аудитория 102	8
3	Аудитория 103	12
\.


--
-- Data for Name: gruppa; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.gruppa (gruppa_id, kurs_id, prepodavatel_id, nazvanie, data_nachala, max_studentov) FROM stdin;
1	1	1	English A1 - Group 1	2025-09-01	5
2	2	2	English A2 - Group 1	2025-09-03	5
3	3	3	Python Beginner	2025-09-05	5
4	4	4	Web Dev Junior	2025-09-07	5
5	7	7	Math OGE	2025-09-02	5
\.


--
-- Data for Name: kategoriya_kursov; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kategoriya_kursov (kategoriya_id, nazvanie, opisanie) FROM stdin;
1	Yazyki	Иностранные языки для детей и взрослых
2	Programmirovanie	Современные IT-курсы
3	Tvorchestvo	Творческие направления и развитие
4	Podgotovka k ekzamenam	ОГЭ и ЕГЭ по основным предметам
\.


--
-- Data for Name: kurs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kurs (kurs_id, kategoriya_id, nazvanie, prodolzhitelnost_chasy, stoimost_mesyac, opisanie) FROM stdin;
1	1	Angliyskiy A1	64	4500.00	Английский язык начального уровня
2	1	Angliyskiy A2	72	5000.00	Уровень pre-intermediate
3	2	Osnovy Python	90	6500.00	Базовое программирование на Python
4	2	Web-razrabotka	100	7000.00	HTML, CSS, JS с нуля
5	3	Risovanie dlya nachinayushchih	40	4000.00	Основы художественного мастерства
6	3	Fotografiya	50	5500.00	Курс творческой фотографии
7	4	Podgotovka k OGE po matematike	80	6000.00	Полный курс подготовки к ОГЭ
\.


--
-- Data for Name: oplata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.oplata (oplata_id, student_id, data, summa, tip_oplaty, kommentariy) FROM stdin;
1	1	2025-09-01	4500.00	karta	Оплата за сентябрь
2	2	2025-09-01	4500.00	online	Оплата за сентябрь
3	3	2025-09-05	6500.00	nal	Оплата за сентябрь
4	4	2025-09-05	6500.00	karta	Оплата за сентябрь
5	5	2025-09-05	7000.00	online	Оплата за сентябрь
6	6	2025-09-07	7000.00	nal	Оплата за сентябрь
7	7	2025-09-07	6000.00	karta	Оплата за сентябрь
8	8	2025-09-07	6000.00	online	Оплата за сентябрь
9	9	2025-09-02	4500.00	nal	Оплата за сентябрь
10	10	2025-09-02	4500.00	karta	Оплата за сентябрь
11	11	2025-09-01	4500.00	online	Оплата за сентябрь
12	12	2025-09-03	5000.00	karta	Оплата за сентябрь
13	13	2025-09-05	6500.00	nal	Оплата за сентябрь
14	14	2025-09-07	7000.00	online	Оплата за сентябрь
15	15	2025-09-02	6000.00	karta	Оплата за сентябрь
\.


--
-- Data for Name: otsenka; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.otsenka (otsenka_id, student_id, kurs_id, znachenie, data, kommentariy) FROM stdin;
\.


--
-- Data for Name: poseshchaemost; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.poseshchaemost (poseshchaemost_id, zanyatie_id, student_id, status) FROM stdin;
1	1	1	present
2	1	2	present
3	1	11	absent
4	2	1	present
5	2	2	late
6	2	11	present
7	3	1	present
8	3	2	present
9	3	11	present
10	4	1	present
11	4	2	absent
12	4	11	present
13	5	1	present
14	5	2	present
15	5	11	present
16	6	1	late
17	6	2	present
18	6	11	present
19	7	3	present
20	7	4	present
21	7	12	present
22	8	3	late
23	8	4	present
24	8	12	present
25	9	3	present
26	9	4	absent
27	9	12	present
28	10	3	present
29	10	4	present
30	10	12	present
31	11	3	present
32	11	4	present
33	11	12	late
34	12	3	present
35	12	4	present
36	12	12	present
37	13	5	present
38	13	6	present
39	13	13	present
40	14	5	present
41	14	6	late
42	14	13	present
43	15	5	absent
44	15	6	present
45	15	13	present
46	16	5	present
47	16	6	present
48	16	13	present
49	17	5	present
50	17	6	present
51	17	13	present
52	18	5	present
53	18	6	present
54	18	13	late
55	19	7	present
56	19	8	present
57	19	14	present
58	20	7	present
59	20	8	present
60	20	14	late
61	21	7	absent
62	21	8	present
63	21	14	present
64	22	7	present
65	22	8	present
66	22	14	present
67	23	7	present
68	23	8	present
69	23	14	present
70	24	7	present
71	24	8	late
72	24	14	present
73	25	9	present
74	25	10	present
75	25	15	present
76	26	9	present
77	26	10	present
78	26	15	present
79	27	9	present
80	27	10	late
81	27	15	present
82	28	9	present
83	28	10	present
84	28	15	present
85	29	9	absent
86	29	10	present
87	29	15	present
88	30	9	present
89	30	10	present
90	30	15	late
\.


--
-- Data for Name: prepodavatel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prepodavatel (prepodavatel_id, familiya, imya, telefon, email, specializaciya, data_nachala) FROM stdin;
1	Ivanova	Anna	89001234501	ivanova.a@mail.ru	Английский язык	2020-09-01
2	Petrova	Elena	89001234502	petrova.e@mail.ru	Английский язык	2019-08-15
3	Smirnov	Dmitriy	89001234503	smirnov.d@mail.ru	Python	2021-01-10
4	Kuznetsov	Igor	89001234504	kuznetsov.i@mail.ru	Web-разработка	2021-03-20
5	Sokolova	Maria	89001234505	sokolova.m@mail.ru	Рисование	2018-11-01
6	Fedorova	Olga	89001234506	fedorova.o@mail.ru	Фотография	2020-02-01
7	Karpov	Nikita	89001234507	karpov.n@mail.ru	Математика ОГЭ	2017-09-05
\.


--
-- Data for Name: roditel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roditel (roditel_id, familiya, imya, telefon, email, rodstvo) FROM stdin;
1	Sidorova	Olga	89006660001	olga.sidorova@mail.ru	mother
2	Kuzmin	Dmitriy	89006660002	dmitriy.kuzmin@mail.ru	father
3	Morozova	Irina	89006660003	irina.morozova@mail.ru	mother
4	Smirnov	Andrey	89006660004	andrey.smirnov@mail.ru	father
5	Petrova	Elena	89006660005	elena.petrova@mail.ru	mother
6	Sokolova	Anna	89006660006	anna.sokolova@mail.ru	mother
7	Volkov	Alexey	89006660007	alexey.volkov@mail.ru	father
8	Kiseleva	Marina	89006660008	marina.kiseleva@mail.ru	mother
9	Belov	Roman	89006660009	roman.belov@mail.ru	father
10	Popova	Ekaterina	89006660010	ekaterina.popova@mail.ru	mother
11	Lebedev	Oleg	89006660011	oleg.lebedev@mail.ru	father
12	Novikova	Svetlana	89006660012	svetlana.novikova@mail.ru	mother
13	Sorokin	Pavel	89006660013	pavel.sorokin@mail.ru	father
14	Filippova	Nadezhda	89006660014	nadezhda.filippova@mail.ru	mother
15	Zaytsev	Anton	89006660015	anton.zaytsev@mail.ru	father
\.


--
-- Data for Name: roditel_student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roditel_student (student_id, roditel_id) FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
11	11
12	12
13	13
14	14
15	15
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student (student_id, familiya, imya, otchestvo, data_rozhdeniya, telefon, email, data_registracii, status) FROM stdin;
1	Sidorov	Maksim	Olegovich	2008-04-12	89005550001	maksim.sidorov@mail.ru	2025-12-04	active
2	Kuzmina	Arina	Dmitrievna	2007-06-22	89005550002	arina.kuzmina@mail.ru	2025-12-04	active
3	Morozov	Egor	Ivanovich	2009-11-01	89005550003	egor.morozov@mail.ru	2025-12-04	active
4	Smirnova	Polina	Andreevna	2010-01-15	89005550004	polina.smirnova@mail.ru	2025-12-04	active
5	Petrov	Ilya	Sergeevich	2008-09-17	89005550005	ilya.petrov@mail.ru	2025-12-04	active
6	Sokolov	Danila	Romanovich	2007-02-03	89005550006	danila.sokolov@mail.ru	2025-12-04	active
7	Volkova	Elizaveta	Alexeevna	2009-03-21	89005550007	elizaveta.volkova@mail.ru	2025-12-04	active
8	Kiselev	Artem	Petrovich	2010-07-05	89005550008	artem.kiselev@mail.ru	2025-12-04	active
9	Belova	Alina	Igorevna	2008-08-26	89005550009	alina.belova@mail.ru	2025-12-04	active
10	Popov	Nikita	Olegovich	2007-12-30	89005550010	nikita.popov@mail.ru	2025-12-04	active
11	Lebedeva	Sofia	Dmitrievna	2009-05-14	89005550011	sofia.lebedeva@mail.ru	2025-12-04	active
12	Novikov	Timur	Alexandrovich	2010-09-08	89005550012	timur.novikov@mail.ru	2025-12-04	active
13	Sorokina	Valeriya	Pavlovna	2008-03-03	89005550013	valeriya.sorokina@mail.ru	2025-12-04	active
14	Filippov	Denis	Ilyich	2007-11-19	89005550014	denis.filippov@mail.ru	2025-12-04	active
15	Zaytseva	Milana	Romanovna	2009-01-28	89005550015	milana.zaytseva@mail.ru	2025-12-04	active
\.


--
-- Data for Name: student_gruppa; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student_gruppa (student_id, gruppa_id, data_zachisleniya, status) FROM stdin;
1	1	2025-09-01	active
2	1	2025-09-01	active
3	2	2025-09-03	active
4	2	2025-09-03	active
5	3	2025-09-05	active
6	3	2025-09-05	active
7	4	2025-09-07	active
8	4	2025-09-07	active
9	5	2025-09-02	active
10	5	2025-09-02	active
11	1	2025-09-01	active
12	2	2025-09-03	active
13	3	2025-09-05	active
14	4	2025-09-07	active
15	5	2025-09-02	active
\.


--
-- Data for Name: zanyatie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.zanyatie (zanyatie_id, gruppa_id, data_vremya, auditoriya_id, tema_zanyatiya) FROM stdin;
1	1	2025-09-02 10:00:00	1	Alphabet and greetings
2	1	2025-09-04 10:00:00	1	Numbers and basic phrases
3	1	2025-09-09 10:00:00	1	Simple sentences
4	1	2025-09-11 10:00:00	1	Family and friends
5	1	2025-09-16 10:00:00	1	Daily routine
6	1	2025-09-18 10:00:00	1	Review
7	2	2025-09-03 12:00:00	2	Present Simple review
8	2	2025-09-05 12:00:00	2	Past Simple introduction
9	2	2025-09-10 12:00:00	2	Future forms
10	2	2025-09-12 12:00:00	2	Vocabulary: hobbies
11	2	2025-09-17 12:00:00	2	Reading comprehension
12	2	2025-09-19 12:00:00	2	Speaking practice
13	3	2025-09-05 14:00:00	3	Variables and types
14	3	2025-09-07 14:00:00	3	If statements
15	3	2025-09-12 14:00:00	3	Loops
16	3	2025-09-14 14:00:00	3	Functions
17	3	2025-09-19 14:00:00	3	Lists and dictionaries
18	3	2025-09-21 14:00:00	3	Project practice
19	4	2025-09-07 16:00:00	1	HTML basics
20	4	2025-09-09 16:00:00	1	CSS basics
21	4	2025-09-14 16:00:00	1	Flexbox and Grid
22	4	2025-09-16 16:00:00	1	JavaScript basics
23	4	2025-09-21 16:00:00	1	DOM manipulation
24	4	2025-09-23 16:00:00	1	Mini project
25	5	2025-09-02 09:00:00	2	Algebra review
26	5	2025-09-04 09:00:00	2	Equations
27	5	2025-09-09 09:00:00	2	Inequalities
28	5	2025-09-11 09:00:00	2	Functions
29	5	2025-09-16 09:00:00	2	Geometry basics
30	5	2025-09-18 09:00:00	2	Review and test
\.


--
-- Name: administrator_administrator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administrator_administrator_id_seq', 1, false);


--
-- Name: auditoriya_auditoriya_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auditoriya_auditoriya_id_seq', 3, true);


--
-- Name: gruppa_gruppa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.gruppa_gruppa_id_seq', 5, true);


--
-- Name: kategoriya_kursov_kategoriya_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kategoriya_kursov_kategoriya_id_seq', 4, true);


--
-- Name: kurs_kurs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kurs_kurs_id_seq', 7, true);


--
-- Name: oplata_oplata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.oplata_oplata_id_seq', 15, true);


--
-- Name: otsenka_otsenka_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.otsenka_otsenka_id_seq', 1, false);


--
-- Name: poseshchaemost_poseshchaemost_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.poseshchaemost_poseshchaemost_id_seq', 95, true);


--
-- Name: prepodavatel_prepodavatel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.prepodavatel_prepodavatel_id_seq', 7, true);


--
-- Name: roditel_roditel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roditel_roditel_id_seq', 15, true);


--
-- Name: student_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_student_id_seq', 15, true);


--
-- Name: zanyatie_zanyatie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.zanyatie_zanyatie_id_seq', 30, true);


--
-- Name: administrator administrator_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrator
    ADD CONSTRAINT administrator_pkey PRIMARY KEY (administrator_id);


--
-- Name: administrator administrator_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.administrator
    ADD CONSTRAINT administrator_username_key UNIQUE (username);


--
-- Name: auditoriya auditoriya_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auditoriya
    ADD CONSTRAINT auditoriya_pkey PRIMARY KEY (auditoriya_id);


--
-- Name: gruppa gruppa_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gruppa
    ADD CONSTRAINT gruppa_pkey PRIMARY KEY (gruppa_id);


--
-- Name: kategoriya_kursov kategoriya_kursov_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kategoriya_kursov
    ADD CONSTRAINT kategoriya_kursov_pkey PRIMARY KEY (kategoriya_id);


--
-- Name: kurs kurs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kurs
    ADD CONSTRAINT kurs_pkey PRIMARY KEY (kurs_id);


--
-- Name: oplata oplata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oplata
    ADD CONSTRAINT oplata_pkey PRIMARY KEY (oplata_id);


--
-- Name: otsenka otsenka_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.otsenka
    ADD CONSTRAINT otsenka_pkey PRIMARY KEY (otsenka_id);


--
-- Name: poseshchaemost poseshchaemost_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.poseshchaemost
    ADD CONSTRAINT poseshchaemost_pkey PRIMARY KEY (poseshchaemost_id);


--
-- Name: poseshchaemost poseshchaemost_zanyatie_id_student_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.poseshchaemost
    ADD CONSTRAINT poseshchaemost_zanyatie_id_student_id_key UNIQUE (zanyatie_id, student_id);


--
-- Name: prepodavatel prepodavatel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prepodavatel
    ADD CONSTRAINT prepodavatel_pkey PRIMARY KEY (prepodavatel_id);


--
-- Name: roditel roditel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roditel
    ADD CONSTRAINT roditel_pkey PRIMARY KEY (roditel_id);


--
-- Name: roditel_student roditel_student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roditel_student
    ADD CONSTRAINT roditel_student_pkey PRIMARY KEY (student_id, roditel_id);


--
-- Name: student student_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_email_key UNIQUE (email);


--
-- Name: student_gruppa student_gruppa_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_gruppa
    ADD CONSTRAINT student_gruppa_pkey PRIMARY KEY (student_id, gruppa_id);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (student_id);


--
-- Name: zanyatie zanyatie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zanyatie
    ADD CONSTRAINT zanyatie_pkey PRIMARY KEY (zanyatie_id);


--
-- Name: gruppa gruppa_kurs_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gruppa
    ADD CONSTRAINT gruppa_kurs_id_fkey FOREIGN KEY (kurs_id) REFERENCES public.kurs(kurs_id) ON DELETE CASCADE;


--
-- Name: gruppa gruppa_prepodavatel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.gruppa
    ADD CONSTRAINT gruppa_prepodavatel_id_fkey FOREIGN KEY (prepodavatel_id) REFERENCES public.prepodavatel(prepodavatel_id) ON DELETE SET NULL;


--
-- Name: kurs kurs_kategoriya_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kurs
    ADD CONSTRAINT kurs_kategoriya_id_fkey FOREIGN KEY (kategoriya_id) REFERENCES public.kategoriya_kursov(kategoriya_id) ON DELETE SET NULL;


--
-- Name: oplata oplata_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oplata
    ADD CONSTRAINT oplata_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(student_id) ON DELETE CASCADE;


--
-- Name: otsenka otsenka_kurs_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.otsenka
    ADD CONSTRAINT otsenka_kurs_id_fkey FOREIGN KEY (kurs_id) REFERENCES public.kurs(kurs_id) ON DELETE CASCADE;


--
-- Name: otsenka otsenka_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.otsenka
    ADD CONSTRAINT otsenka_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(student_id) ON DELETE CASCADE;


--
-- Name: poseshchaemost poseshchaemost_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.poseshchaemost
    ADD CONSTRAINT poseshchaemost_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(student_id) ON DELETE CASCADE;


--
-- Name: poseshchaemost poseshchaemost_zanyatie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.poseshchaemost
    ADD CONSTRAINT poseshchaemost_zanyatie_id_fkey FOREIGN KEY (zanyatie_id) REFERENCES public.zanyatie(zanyatie_id) ON DELETE CASCADE;


--
-- Name: roditel_student roditel_student_roditel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roditel_student
    ADD CONSTRAINT roditel_student_roditel_id_fkey FOREIGN KEY (roditel_id) REFERENCES public.roditel(roditel_id) ON DELETE CASCADE;


--
-- Name: roditel_student roditel_student_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roditel_student
    ADD CONSTRAINT roditel_student_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(student_id) ON DELETE CASCADE;


--
-- Name: student_gruppa student_gruppa_gruppa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_gruppa
    ADD CONSTRAINT student_gruppa_gruppa_id_fkey FOREIGN KEY (gruppa_id) REFERENCES public.gruppa(gruppa_id) ON DELETE CASCADE;


--
-- Name: student_gruppa student_gruppa_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.student_gruppa
    ADD CONSTRAINT student_gruppa_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.student(student_id) ON DELETE CASCADE;


--
-- Name: zanyatie zanyatie_auditoriya_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zanyatie
    ADD CONSTRAINT zanyatie_auditoriya_id_fkey FOREIGN KEY (auditoriya_id) REFERENCES public.auditoriya(auditoriya_id) ON DELETE SET NULL;


--
-- Name: zanyatie zanyatie_gruppa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zanyatie
    ADD CONSTRAINT zanyatie_gruppa_id_fkey FOREIGN KEY (gruppa_id) REFERENCES public.gruppa(gruppa_id) ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA public TO unium_user;


--
-- Name: TABLE administrator; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.administrator TO unium_user;


--
-- Name: TABLE auditoriya; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.auditoriya TO unium_user;


--
-- Name: TABLE gruppa; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.gruppa TO unium_user;


--
-- Name: TABLE kategoriya_kursov; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.kategoriya_kursov TO unium_user;


--
-- Name: TABLE kurs; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.kurs TO unium_user;


--
-- Name: TABLE oplata; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.oplata TO unium_user;


--
-- Name: TABLE otsenka; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.otsenka TO unium_user;


--
-- Name: TABLE poseshchaemost; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.poseshchaemost TO unium_user;


--
-- Name: TABLE prepodavatel; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.prepodavatel TO unium_user;


--
-- Name: TABLE roditel; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.roditel TO unium_user;


--
-- Name: TABLE roditel_student; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.roditel_student TO unium_user;


--
-- Name: TABLE student; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.student TO unium_user;


--
-- Name: TABLE student_gruppa; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.student_gruppa TO unium_user;


--
-- Name: TABLE zanyatie; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.zanyatie TO unium_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES  TO unium_user;


--
-- PostgreSQL database dump complete
--

\unrestrict kGW9TFVQIeO279vjCNQcHyjD1vpGJ9b9iBIfyP8pnxYqwhaiCPdMnCLWWxgwDcI

