/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2012-12-21 16:14:58                          */
/*==============================================================*/


drop table if exists px_link;

drop table if exists px_option;

drop table if exists px_post;

drop table if exists px_post_tag;

drop table if exists px_tag;

/*==============================================================*/
/* Table: px_link                                               */
/*==============================================================*/
create table px_link
(
   id                   int not null auto_increment,
   name                 varchar(50) not null,
   sort                 int default 0,
   description          varchar(500),
   url                  varchar(200) not null,
   icon                 varchar(200),
   status               varchar(20) not null default 'hidden',
   primary key (id),
   unique key UNI_LINK_NAME (name),
   unique key UNI_LINK_URL (url)
);

/*==============================================================*/
/* Table: px_option                                             */
/*==============================================================*/
create table px_option
(
   id                   int not null auto_increment,
   name                 varchar(100) not null,
   value                longtext not null,
   description          varchar(200),
   primary key (id),
   unique key UNI_OPTION_NAME (name)
);

/*==============================================================*/
/* Table: px_post                                               */
/*==============================================================*/
create table px_post
(
   id                   int not null auto_increment,
   url                  varchar(200),
   title                varchar(500),
   content              longtext not null,
   addtime              int(10) not null,
   top                  int not null default 0,
   status               varchar(20) not null default 'publish',
   type                 varchar(20) not null default 'post',
   password             varchar(10),
   primary key (id)
);

/*==============================================================*/
/* Table: px_post_tag                                           */
/*==============================================================*/
create table px_post_tag
(
   post_id              int not null,
   tag_id               int not null,
   primary key (post_id, tag_id)
);

/*==============================================================*/
/* Table: px_tag                                                */
/*==============================================================*/
create table px_tag
(
   id                   int not null auto_increment,
   name                 varchar(50) not null,
   sort                 int default 0,
   post_count           int default 0,
   primary key (id),
   unique key UNI_TAG_NAME (name)
);

alter table px_post_tag add constraint FK_TO_POST foreign key (post_id)
      references px_post (id) on delete restrict on update restrict;

alter table px_post_tag add constraint FK_TO_TAG foreign key (tag_id)
      references px_tag (id) on delete restrict on update restrict;

