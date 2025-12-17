--
-- PostgreSQL database dump
--

\restrict Z6imGfbZhddy7MBmTMc0GfwPAmPPD7L6o96WL9WGCaSGD54BPYwxHShcqxAsmqR

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2025-12-16 19:55:20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 230 (class 1255 OID 16638)
-- Name: update_account_balance(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_account_balance() RETURNS trigger
    LANGUAGE plpgsql SECURITY DEFINER
    AS $$
BEGIN
    IF NEW.operation_type = 'доход' THEN
        UPDATE accounts
        SET balance = balance + NEW.amount
        WHERE account_id = NEW.account_id;
    ELSE
        UPDATE accounts
        SET balance = balance - NEW.amount
        WHERE account_id = NEW.account_id;
    END IF;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_account_balance() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 224 (class 1259 OID 16566)
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    account_id integer NOT NULL,
    user_id integer NOT NULL,
    account_name text NOT NULL,
    balance numeric(12,2) DEFAULT 0 NOT NULL,
    currency_id integer NOT NULL,
    CONSTRAINT balance_non_negative CHECK ((balance >= (0)::numeric))
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16565)
-- Name: accounts_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accounts_account_id_seq OWNER TO postgres;

--
-- TOC entry 4985 (class 0 OID 0)
-- Dependencies: 223
-- Name: accounts_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_account_id_seq OWNED BY public.accounts.account_id;


--
-- TOC entry 226 (class 1259 OID 16591)
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    category_id integer NOT NULL,
    category_name text NOT NULL,
    category_type text NOT NULL,
    CONSTRAINT categories_category_type_check CHECK ((category_type = ANY (ARRAY['доход'::text, 'расход'::text])))
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16590)
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_category_id_seq OWNER TO postgres;

--
-- TOC entry 4988 (class 0 OID 0)
-- Dependencies: 225
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;


--
-- TOC entry 220 (class 1259 OID 16538)
-- Name: currency; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.currency (
    currency_id integer NOT NULL,
    code character(3) NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.currency OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16537)
-- Name: currency_currency_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.currency_currency_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.currency_currency_id_seq OWNER TO postgres;

--
-- TOC entry 4990 (class 0 OID 0)
-- Dependencies: 219
-- Name: currency_currency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.currency_currency_id_seq OWNED BY public.currency.currency_id;


--
-- TOC entry 228 (class 1259 OID 16606)
-- Name: operations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.operations (
    operation_id integer NOT NULL,
    operation_date date DEFAULT CURRENT_DATE NOT NULL,
    amount numeric(12,2) NOT NULL,
    operation_type text NOT NULL,
    user_id integer NOT NULL,
    account_id integer NOT NULL,
    category_id integer NOT NULL,
    CONSTRAINT operations_amount_check CHECK ((amount > (0)::numeric)),
    CONSTRAINT operations_operation_type_check CHECK ((operation_type = ANY (ARRAY['доход'::text, 'расход'::text])))
);


ALTER TABLE public.operations OWNER TO postgres;

--
-- TOC entry 4992 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE operations; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.operations IS 'Таблица финансовых операций';


--
-- TOC entry 4993 (class 0 OID 0)
-- Dependencies: 228
-- Name: COLUMN operations.amount; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operations.amount IS 'Сумма операции';


--
-- TOC entry 4994 (class 0 OID 0)
-- Dependencies: 228
-- Name: COLUMN operations.operation_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.operations.operation_type IS 'Тип операции: доход или расход';


--
-- TOC entry 227 (class 1259 OID 16605)
-- Name: operations_operation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.operations_operation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.operations_operation_id_seq OWNER TO postgres;

--
-- TOC entry 4996 (class 0 OID 0)
-- Dependencies: 227
-- Name: operations_operation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.operations_operation_id_seq OWNED BY public.operations.operation_id;


--
-- TOC entry 222 (class 1259 OID 16552)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16644)
-- Name: operations_view; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.operations_view AS
 SELECT o.operation_date,
    o.operation_type,
    o.amount,
    c.category_name,
    a.account_name,
    u.username
   FROM (((public.operations o
     JOIN public.categories c ON ((o.category_id = c.category_id)))
     JOIN public.accounts a ON ((o.account_id = a.account_id)))
     JOIN public.users u ON ((o.user_id = u.user_id)));


ALTER VIEW public.operations_view OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16551)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 4999 (class 0 OID 0)
-- Dependencies: 221
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 4783 (class 2604 OID 16569)
-- Name: accounts account_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts ALTER COLUMN account_id SET DEFAULT nextval('public.accounts_account_id_seq'::regclass);


--
-- TOC entry 4785 (class 2604 OID 16594)
-- Name: categories category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);


--
-- TOC entry 4780 (class 2604 OID 16541)
-- Name: currency currency_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currency ALTER COLUMN currency_id SET DEFAULT nextval('public.currency_currency_id_seq'::regclass);


--
-- TOC entry 4786 (class 2604 OID 16609)
-- Name: operations operation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations ALTER COLUMN operation_id SET DEFAULT nextval('public.operations_operation_id_seq'::regclass);


--
-- TOC entry 4781 (class 2604 OID 16555)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 4974 (class 0 OID 16566)
-- Dependencies: 224
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts (account_id, user_id, account_name, balance, currency_id) FROM stdin;
1	1	Основной счёт	100243.00	1
\.


--
-- TOC entry 4976 (class 0 OID 16591)
-- Dependencies: 226
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (category_id, category_name, category_type) FROM stdin;
1	Зарплата	доход
\.


--
-- TOC entry 4970 (class 0 OID 16538)
-- Dependencies: 220
-- Data for Name: currency; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.currency (currency_id, code, name) FROM stdin;
1	RUB	Российский рубль
\.


--
-- TOC entry 4978 (class 0 OID 16606)
-- Dependencies: 228
-- Data for Name: operations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.operations (operation_id, operation_date, amount, operation_type, user_id, account_id, category_id) FROM stdin;
2	2025-10-15	50000.00	доход	1	1	1
3	2025-11-14	50243.00	доход	1	1	1
\.


--
-- TOC entry 4972 (class 0 OID 16552)
-- Dependencies: 222
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, created_at) FROM stdin;
1	test_user	2025-12-16 19:25:42.921799
\.


--
-- TOC entry 5001 (class 0 OID 0)
-- Dependencies: 223
-- Name: accounts_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_account_id_seq', 1, true);


--
-- TOC entry 5002 (class 0 OID 0)
-- Dependencies: 225
-- Name: categories_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_category_id_seq', 1, true);


--
-- TOC entry 5003 (class 0 OID 0)
-- Dependencies: 219
-- Name: currency_currency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.currency_currency_id_seq', 1, true);


--
-- TOC entry 5004 (class 0 OID 0)
-- Dependencies: 227
-- Name: operations_operation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.operations_operation_id_seq', 3, true);


--
-- TOC entry 5005 (class 0 OID 0)
-- Dependencies: 221
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- TOC entry 4801 (class 2606 OID 16579)
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (account_id);


--
-- TOC entry 4803 (class 2606 OID 16604)
-- Name: categories categories_category_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_category_name_key UNIQUE (category_name);


--
-- TOC entry 4805 (class 2606 OID 16602)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- TOC entry 4793 (class 2606 OID 16550)
-- Name: currency currency_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_code_key UNIQUE (code);


--
-- TOC entry 4795 (class 2606 OID 16548)
-- Name: currency currency_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (currency_id);


--
-- TOC entry 4811 (class 2606 OID 16622)
-- Name: operations operations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations
    ADD CONSTRAINT operations_pkey PRIMARY KEY (operation_id);


--
-- TOC entry 4797 (class 2606 OID 16562)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4799 (class 2606 OID 16564)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4806 (class 1259 OID 16641)
-- Name: idx_operations_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_operations_account_id ON public.operations USING btree (account_id);


--
-- TOC entry 4807 (class 1259 OID 16642)
-- Name: idx_operations_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_operations_category_id ON public.operations USING btree (category_id);


--
-- TOC entry 4808 (class 1259 OID 16643)
-- Name: idx_operations_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_operations_date ON public.operations USING btree (operation_date);


--
-- TOC entry 4809 (class 1259 OID 16640)
-- Name: idx_operations_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_operations_user_id ON public.operations USING btree (user_id);


--
-- TOC entry 4820 (class 2620 OID 16650)
-- Name: operations trg_update_balance; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_update_balance AFTER INSERT ON public.operations FOR EACH ROW EXECUTE FUNCTION public.update_account_balance();


--
-- TOC entry 4812 (class 2606 OID 16585)
-- Name: accounts fk_account_currency; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT fk_account_currency FOREIGN KEY (currency_id) REFERENCES public.currency(currency_id) ON DELETE RESTRICT;


--
-- TOC entry 4813 (class 2606 OID 16580)
-- Name: accounts fk_account_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT fk_account_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE RESTRICT;


--
-- TOC entry 4814 (class 2606 OID 16663)
-- Name: accounts fk_accounts_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT fk_accounts_user FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 4815 (class 2606 OID 16628)
-- Name: operations fk_operation_account; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations
    ADD CONSTRAINT fk_operation_account FOREIGN KEY (account_id) REFERENCES public.accounts(account_id) ON DELETE RESTRICT;


--
-- TOC entry 4816 (class 2606 OID 16633)
-- Name: operations fk_operation_category; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations
    ADD CONSTRAINT fk_operation_category FOREIGN KEY (category_id) REFERENCES public.categories(category_id) ON DELETE RESTRICT;


--
-- TOC entry 4817 (class 2606 OID 16623)
-- Name: operations fk_operation_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations
    ADD CONSTRAINT fk_operation_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE RESTRICT;


--
-- TOC entry 4818 (class 2606 OID 16658)
-- Name: operations fk_operations_category; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations
    ADD CONSTRAINT fk_operations_category FOREIGN KEY (category_id) REFERENCES public.categories(category_id);


--
-- TOC entry 4819 (class 2606 OID 16653)
-- Name: operations fk_operations_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.operations
    ADD CONSTRAINT fk_operations_user FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 4984 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE accounts; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.accounts TO finance_app;


--
-- TOC entry 4986 (class 0 OID 0)
-- Dependencies: 223
-- Name: SEQUENCE accounts_account_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.accounts_account_id_seq TO finance_app;


--
-- TOC entry 4987 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE categories; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.categories TO finance_app;


--
-- TOC entry 4989 (class 0 OID 0)
-- Dependencies: 225
-- Name: SEQUENCE categories_category_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.categories_category_id_seq TO finance_app;


--
-- TOC entry 4991 (class 0 OID 0)
-- Dependencies: 219
-- Name: SEQUENCE currency_currency_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.currency_currency_id_seq TO finance_app;


--
-- TOC entry 4995 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE operations; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,INSERT ON TABLE public.operations TO finance_app;


--
-- TOC entry 4997 (class 0 OID 0)
-- Dependencies: 227
-- Name: SEQUENCE operations_operation_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.operations_operation_id_seq TO finance_app;


--
-- TOC entry 4998 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE users; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.users TO finance_app;


--
-- TOC entry 5000 (class 0 OID 0)
-- Dependencies: 221
-- Name: SEQUENCE users_user_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.users_user_id_seq TO finance_app;


-- Completed on 2025-12-16 19:55:20

--
-- PostgreSQL database dump complete
--

\unrestrict Z6imGfbZhddy7MBmTMc0GfwPAmPPD7L6o96WL9WGCaSGD54BPYwxHShcqxAsmqR

