# -*- coding: utf-8 -*-
import pandas as pd
import tkinter.filedialog as filedialog
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import create_engine, URL, String, ForeignKey
from sqlalchemy.dialects.postgresql import insert
from functools import reduce

# Define functions


def load_csv_files():
    # Open multiple files using the dialog box
    file_paths = filedialog.askopenfilenames(
        title="Select CSV files", filetypes=[("CSV Files", "*.csv")])

    if not file_paths:  # Check if no files were selected
        print("No files selected.")
        return None

    # Read each file into a DataFrame and concatenate them
    dataframes = [pd.read_csv(file) for file in file_paths]
    combined_df = reduce(lambda left, right: pd.concat(
        [left, right], ignore_index=True), dataframes)

    combined_df = combined_df[(combined_df["Cod. Settore Docente"] == "ICAR/17") |
                              ((combined_df["Cod. Ruolo"] == "0000") & (combined_df["Settore"] == "ICAR/17"))]

    combined_df["Cod. Settore Docente"] = combined_df["Cod. Settore Docente"].fillna(
        "ICAR/17")

    combined_df = combined_df.dropna(subset=['Cognome'])

    return combined_df


df = load_csv_files()

# Create an engine
url_object = URL.create(
    "postgresql+psycopg",
    username="my-username",
    password="my-password",
    host="localhost",
    database="my-db",
)

engine = create_engine(url_object)


# Setting up MetaData with Table classes


class Base(DeclarativeBase):
    pass


Base.metadata
Base.registry


class Dipartimenti(Base):
    __tablename__ = "Dipartimenti"

    codice: Mapped[str] = mapped_column(String(15), primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))

    def __init__(self, codice, nome):
        self.codice = codice
        self.nome = nome

    def __repr__(self) -> str:
        return f"<Dipartimento(codice={self.codice}, nome={self.nome})>"


class CdL(Base):
    __tablename__ = "CdL"

    codice: Mapped[str] = mapped_column(String(10), primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    laurea: Mapped[str]
    dipartimento: Mapped[str] = mapped_column(
        String(15), ForeignKey("Dipartimenti.codice"))

    def __init__(self, codice, nome, laurea, dipartimento):
        self.codice = codice
        self.nome = nome
        self.laurea = laurea
        self.dipartimento = dipartimento

    def __repr__(self) -> str:
        return f"CdL(codice={self.codice!r}, nome={self.nome!r}, laurea={self.laurea!r}, dipartimento={self.dipartimento!r})"


class SSD(Base):
    __tablename__ = "SSD"

    codice: Mapped[str] = mapped_column(String(10), primary_key=True)
    dipartimento: Mapped[str] = mapped_column(
        String(15), ForeignKey("Dipartimenti.codice"))

    def __init__(self, codice, dipartimento):
        self.codice = codice
        self.dipartimento = dipartimento

    def __repr__(self) -> str:
        return f"SSD(codice={self.codice!r}, dipartimento={self.dipartimento!r})"


class Esami(Base):
    __tablename__ = "Esami"

    codice: Mapped[str] = mapped_column(String(10), primary_key=True)
    cdl_codice: Mapped[str] = mapped_column(
        String(10), ForeignKey("CdL.codice"))
    insegnamento: Mapped[str]
    cfu: Mapped[str]
    ssd_aff: Mapped[str] = mapped_column(String(10), ForeignKey("SSD.codice"))

    def __init__(self, codice, cdl_codice, insegnamento, cfu, ssd_aff):
        self.codice = codice
        self.cdl_codice = cdl_codice
        self.insegnamento = insegnamento
        self.cfu = cfu
        self.ssd_aff = ssd_aff

    def __repr__(self) -> str:
        return f"Esami(codice={self.codice!r}, cdl_codice={self.cdl_codice!r}, insegnamento={self.insegnamento!r}, cfu={self.cfu!r}, ssd_aff={self.ssd_aff!r})"


class PersonaleStrutturato(Base):
    __tablename__ = "PersonaleStrutturato"

    matricola: Mapped[str] = mapped_column(String(10), primary_key=True)
    cognome: Mapped[str] = mapped_column(nullable=False)
    cod_fisc: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    ssd_doc: Mapped[str] = mapped_column(
        String(10), ForeignKey("SSD.codice"), nullable=True)

    settore_docente_relationship = relationship("SSD")

    def __init__(self, matricola, cognome, cod_fisc, nome, ssd_doc):
        self.matricola = matricola
        self.cognome = cognome
        self.cod_fisc = cod_fisc
        self.nome = nome
        self.ssd_doc = ssd_doc

    def __repr__(self) -> str:
        return f"PersonaleStrutturato(matricola={self.matricola!r}, cognome={self.cognome!r}, cod_fisc={self.cod_fisc!r}, nome={self.nome!r}, ssd_doc={self.ssd_doc!r})"


class TipologiaAffidamento(Base):
    __tablename__ = "TipologiaAffidamento"

    codice: Mapped[str] = mapped_column(String(10), primary_key=True)
    descrizione: Mapped[str] = mapped_column(nullable=True)
    note: Mapped[str] = mapped_column(nullable=True)

    def __init__(self, codice, descrizione, note):
        self.codice = codice
        self.descrizione = descrizione
        self.note = note

    def __repr__(self) -> str:
        return f"TipologiaAffidamento(codice={self.codice!r}, descrizione={self.descrizione!r}, note={self.note!r})"


class TipologiaContratti(Base):
    __tablename__ = "TipologiaContratti"

    codice: Mapped[str] = mapped_column(primary_key=True)
    descrizione: Mapped[str] = mapped_column(nullable=True)
    note: Mapped[str] = mapped_column(nullable=True)

    def __init__(self, codice, descrizione, note):
        self.codice = codice
        self.descrizione = descrizione
        self.note = note

    def __repr__(self) -> str:
        return f"TipologiaContratti(codice={self.codice!r}, descrizione={self.descrizione!r}, note={self.note!r})"


class Affidamenti(Base):
    __tablename__ = "Affidamenti"

    id_copertura: Mapped[str] = mapped_column(primary_key=True)
    anno: Mapped[int] = mapped_column(nullable=False)
    docente: Mapped[str] = mapped_column(
        ForeignKey("PersonaleStrutturato.matricola"))
    docente_cat: Mapped[str] = mapped_column(
        ForeignKey("TipologiaContratti.codice"))
    corso: Mapped[str] = mapped_column(ForeignKey("Esami.codice"))
    cfu_copertura: Mapped[float]
    ore_copertura: Mapped[float]
    tip_aff: Mapped[str] = mapped_column(
        ForeignKey("TipologiaAffidamento.codice"))
    lettere: Mapped[str]
    cdl: Mapped[str] = mapped_column(ForeignKey("CdL.codice"))

    rel_docente = relationship("PersonaleStrutturato")
    rel_contratto = relationship("TipologiaContratti")
    rel_esame = relationship("Esami")
    rel_tipaff = relationship("TipologiaAffidamento")
    rel_cdl = relationship("CdL")

    def __init__(self, id_copertura, anno, docente, docente_cat, corso, cfu_copertura, ore_copertura, tip_aff, lettere, cdl):
        self.id_copertura = id_copertura
        self.anno = anno
        self.docente = docente
        self.docente_cat = docente_cat
        self.corso = corso
        self.cfu_copertura = cfu_copertura
        self.ore_copertura = ore_copertura
        self.tip_aff = tip_aff
        self.lettere = lettere
        self.cdl = cdl

    def __repr__(self) -> str:
        return f"Affidamenti(id_copertura={self.id_copertura!r}, anno={self.anno!r}, docente={self.docente!r}, docente_cat={self.docente_cat!r}, corso={self.corso!r}, cfu_copertura={self.cfu_copertura!r}, ore_copertura={self.ore_copertura!r}, tip_aff={self.tip_aff!r}, lettere={self.lettere!r}, cdl={self.cdl!r})"


Base.metadata.create_all(engine)

# Insert value
Session = sessionmaker(engine)

# Get unique department codes
unique_dip_ids = df['Cod. Dipartimento'].unique()
dict_dip = {}

for dip_id in unique_dip_ids:
    df_filtered = df[df['Cod. Dipartimento'] == dip_id]

    if not df_filtered.empty:
        info = {}

        info['dip_id'] = str(dip_id)
        info['dip_name'] = df_filtered['Des. Dipartimento'].iloc[0]

        dict_dip[dip_id] = info


for key, value in dict_dip.items():
    with Session.begin() as session:
        value_Dipartimenti = insert(Dipartimenti).values(codice=value['dip_id'], nome=value['dip_name'])
        session.execute(value_Dipartimenti.on_conflict_do_nothing(index_elements=['codice']))
        session.commit()

unique_cdl_ids = df['Cod. Corso di Studio'].unique()  # Get unique CdL codes
dict_cdl = {}

for cdl_id in unique_cdl_ids:
    df_filtered = df[df['Cod. Corso di Studio'] == cdl_id]

    if not df_filtered.empty:
        info = {}

        info['cdl_id'] = str(cdl_id)
        info['cdl_name'] = df_filtered['Des. Corso di Studio'].iloc[0]
        info['cdl_degree'] = df_filtered['Cod. Tipo Corso'].iloc[0]
        info['cdl_dep'] = str(df_filtered['Cod. Dipartimento'].iloc[0])

        dict_cdl[cdl_id] = info

for key, value in dict_cdl.items():
    with Session.begin() as session:
        value_CdL = insert(CdL).values(codice=value['cdl_id'], nome=value['cdl_name'],
                        laurea=value['cdl_degree'], dipartimento=value['cdl_dep'])
        session.execute(value_CdL.on_conflict_do_nothing(index_elements=['codice']))
        session.commit()

unique_ssd_ids = df['Settore'].unique()  # Get unique SSD codes
dict_ssd = {}

for ssd_id in unique_ssd_ids:
    df_filtered = df[df['Settore'] == ssd_id]

    if not df_filtered.empty:
        info = {}

        info['ssd_id'] = ssd_id
        info['ssd_dep'] = df_filtered['Cod. Dipartimento'].iloc[0]

        # Store information for this course code in the main dictionar
        dict_ssd[ssd_id] = info

for key, value in dict_ssd.items():
    with Session.begin() as session:
        value_SSD = insert(SSD).values(codice=value['ssd_id'], dipartimento=value['ssd_dep'])
        session.execute(value_SSD.on_conflict_do_nothing(index_elements=['codice']))
        session.commit()

unique_exam_ids = df['Cod. Att. Form.'].unique()  # Get unique Exam codes
dict_exam = {}

for exam_id in unique_exam_ids:
    df_filtered = df[df['Cod. Att. Form.'] == exam_id]

    if not df_filtered.empty:
        info = {}

        info['exam_id'] = exam_id
        info['exam_degree'] = str(df_filtered['Cod. Corso di Studio'].iloc[0])
        info['exam_name'] = df_filtered['Des. Insegnamento'].iloc[0]
        info['exam_cfu'] = str(df_filtered['Peso Insegnamento'].iloc[0])
        info['exam_ssd'] = df_filtered['Settore'].iloc[0]

        dict_exam[exam_id] = info

for key, value in dict_exam.items():
    with Session.begin() as session:
        value_Exam = insert(Esami).values(codice=value['exam_id'], cdl_codice=value['exam_degree'],
                           insegnamento=value['exam_name'], cfu=value['exam_cfu'], ssd_aff=value['exam_ssd'])
        session.execute(value_Exam.on_conflict_do_nothing(index_elements=['codice']))
        session.commit()

unique_prof_ids = df['Matricola'].unique()  # Get unique Professor codes
dict_prof = {}

for prof_id in unique_prof_ids:
    df_filtered = df[df['Matricola'] == prof_id]

    if not df_filtered.empty:
        info = {}

        info['prof_id'] = str(prof_id).replace(".0", "")
        info['prof_surname'] = df_filtered['Cognome'].iloc[0]
        info['prof_name'] = df_filtered['Nome'].iloc[0]
        info['prof_ssn'] = df_filtered['Cod. Fiscale'].iloc[0]
        info['prof_ssd'] = str(df_filtered['Cod. Settore Docente'].iloc[0])

        dict_prof[prof_id] = info

for key, value in dict_prof.items():
    with Session.begin() as session:
        value_Prof = insert(PersonaleStrutturato).values(matricola=value['prof_id'], cognome=value['prof_surname'],
                                          cod_fisc=value['prof_name'], nome=value['prof_ssn'], ssd_doc=value['prof_ssd'])
        session.execute(value_Prof.on_conflict_do_nothing(index_elements=['matricola']))
        session.commit()

# Get unique TipologiaAfferenza codes
unique_typeaff_ids = df['Cod. Tipo Coper.'].unique()
dict_typeaff = {}

for typeaff_id in unique_typeaff_ids:
    df_filtered = df[df['Cod. Tipo Coper.'] == typeaff_id]

    if not df_filtered.empty:
        info = {}

        info['typeaff_id'] = typeaff_id
        info['afftype_description'] = ""
        info['afftype_note'] = ""

        dict_typeaff[typeaff_id] = info

for key, value in dict_typeaff.items():
    with Session.begin() as session:
        value_TypeAff = insert(TipologiaAffidamento).values(
            codice=value['typeaff_id'], descrizione=value['afftype_description'], note=value['afftype_note'])
        session.execute(value_TypeAff.on_conflict_do_nothing(index_elements=['codice']))
        session.commit()


unique_contract_ids = df['Cod. Ruolo'].unique()  # Get unique Contract codes
dict_contract = {}

for contract_id in unique_contract_ids:
    df_filtered = df[df['Cod. Ruolo'] == contract_id]

    if not df_filtered.empty:
        info = {}

        info['contract_id'] = contract_id
        info['contract_description'] = ""
        info['contract_note'] = ""

        dict_contract[contract_id] = info

for key, value in dict_contract.items():
    with Session.begin() as session:
        value_Contract = insert(TipologiaContratti).values(
            codice=value['contract_id'], descrizione=value['contract_description'], note=value['contract_note'])
        session.execute(value_Contract.on_conflict_do_nothing(index_elements=['codice']))
        session.commit()


unique_aff_ids = df['Id. Copertura'].unique()  # Get unique Affidamento codes
dict_aff = {}

for aff_id in unique_aff_ids:
    df_filtered = df[df['Id. Copertura'] == aff_id]

    if not df_filtered.empty:
        info = {}

        info['aff_id'] = int(aff_id)
        info['aff_year'] = int(df_filtered['Anno Offerta'].iloc[0])
        info['aff_prof'] = str(
            df_filtered['Matricola'].iloc[0]).replace(".0", "")
        info['aff_catprof'] = df_filtered['Cod. Ruolo'].iloc[0]
        info['aff_exam'] = df_filtered['Cod. Att. Form.'].iloc[0]
        info['aff_cfu'] = float(df_filtered['Peso'].iloc[0])
        info['aff_hours'] = float(df_filtered['Ore Coper.'].iloc[0])
        info['aff_type'] = df_filtered['Cod. Tipo Coper.'].iloc[0]
        info['aff_letters'] = df_filtered['Cod. Partizione Studenti'].iloc[0]
        info['aff_cdl'] = str(df_filtered['Cod. Corso di Studio'].iloc[0])

        dict_aff[aff_id] = info

for key, value in dict_aff.items():
    with Session.begin() as session:
        value_Aff = insert(Affidamenti).values(id_copertura=value['aff_id'], anno=value['aff_year'], docente=value['aff_prof'], docente_cat=value['aff_catprof'], corso=value['aff_exam'],
                                cfu_copertura=value['aff_cfu'], ore_copertura=value['aff_hours'], tip_aff=value['aff_type'], lettere=value['aff_letters'], cdl=value['aff_cdl'])
        session.execute(value_Aff.on_conflict_do_nothing(index_elements=['id_copertura']))
        session.commit()
