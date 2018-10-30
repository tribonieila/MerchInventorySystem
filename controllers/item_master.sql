
CREATE TABLE public."Item_Master"
(
    id integer NOT NULL DEFAULT nextval('"Item_Master_id_seq"'::regclass),
    supplier_item_ref character varying(20) COLLATE pg_catalog."default",
    int_barcode character varying(20) COLLATE pg_catalog."default",
    loc_barcode character varying(20) COLLATE pg_catalog."default",
    purchase_point integer,
    uom_value integer,
    uom_id integer,
    supplier_uom_value integer,
    supplier_uom_id integer,
    weight_value integer,
    weight_id integer,
    type_id integer,
    division_id integer,
    dept_code_id integer,
    supplier_code_id integer,
    product_code_id integer,
    subproduct_code_id integer,
    group_line_id integer,
    brand_line_code_id integer,
    brand_cls_code_id integer,
    section_code_id integer,
    size_code_id integer,
    gender_code_id integer,
    fragrance_code_id integer,
    color_code_id integer,
    collection_code_id integer,
    made_in_id integer,
    item_status_code_id integer,
    created_on timestamp without time zone,
    created_by integer,
    updated_on timestamp without time zone,
    updated_by integer,
    item_code character varying(15) COLLATE pg_catalog."default",
    item_description_ar character varying(50) COLLATE pg_catalog."default",
    item_description character varying(50) COLLATE pg_catalog."default",
    selective_tax character varying(25) COLLATE pg_catalog."default",
    vat_percentage character varying(25) COLLATE pg_catalog."default",
    CONSTRAINT "Item_Master_pkey" PRIMARY KEY (id),
    CONSTRAINT "Item_Master_brand_cls_code_id_fkey" FOREIGN KEY (brand_cls_code_id)
        REFERENCES public."Brand_Classification" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_brand_line_code_id_fkey" FOREIGN KEY (brand_line_code_id)
        REFERENCES public."Brand_Line" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_collection_code_id_fkey" FOREIGN KEY (collection_code_id)
        REFERENCES public."Item_Collection" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_color_code_id_fkey" FOREIGN KEY (color_code_id)
        REFERENCES public."Color_Code" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_created_by_fkey" FOREIGN KEY (created_by)
        REFERENCES public.auth_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_dept_code_id_fkey" FOREIGN KEY (dept_code_id)
        REFERENCES public."Department" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_division_id_fkey" FOREIGN KEY (division_id)
        REFERENCES public."Division" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_fragrance_code_id_fkey" FOREIGN KEY (fragrance_code_id)
        REFERENCES public."Fragrance_Type" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_gender_code_id_fkey" FOREIGN KEY (gender_code_id)
        REFERENCES public."Gender" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_group_line_id_fkey" FOREIGN KEY (group_line_id)
        REFERENCES public."GroupLine" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_item_status_code_id_fkey" FOREIGN KEY (item_status_code_id)
        REFERENCES public."Status" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_made_in_id_fkey" FOREIGN KEY (made_in_id)
        REFERENCES public."Made_In" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_product_code_id_fkey" FOREIGN KEY (product_code_id)
        REFERENCES public."Product" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_section_code_id_fkey" FOREIGN KEY (section_code_id)
        REFERENCES public."Section" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_size_code_id_fkey" FOREIGN KEY (size_code_id)
        REFERENCES public."Item_Size" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_subproduct_code_id_fkey" FOREIGN KEY (subproduct_code_id)
        REFERENCES public."SubProduct" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_supplier_code_id_fkey" FOREIGN KEY (supplier_code_id)
        REFERENCES public."Supplier_Master" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_supplier_uom_id_fkey" FOREIGN KEY (supplier_uom_id)
        REFERENCES public."Supplier_UOM" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_type_id_fkey" FOREIGN KEY (type_id)
        REFERENCES public."Item_Type" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_uom_id_fkey" FOREIGN KEY (uom_id)
        REFERENCES public."UOM" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "Item_Master_updated_by_fkey" FOREIGN KEY (updated_by)
        REFERENCES public.auth_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)