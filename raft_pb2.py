# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: raft.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'raft.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\x12\x06raftkv\"\'\n\x05State\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08isLeader\x18\x02 \x01(\x08\"K\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\x10\n\x08\x43lientId\x18\x03 \x01(\x03\x12\x11\n\tRequestId\x18\x04 \x01(\x03\":\n\x06GetKey\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x10\n\x08\x43lientId\x18\x02 \x01(\x03\x12\x11\n\tRequestId\x18\x03 \x01(\x03\":\n\x05Reply\x12\x13\n\x0bwrongLeader\x18\x01 \x01(\x08\x12\r\n\x05\x65rror\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\x19\n\nIntegerArg\x12\x0b\n\x03\x61rg\x18\x01 \x01(\x05\"\x18\n\tStringArg\x12\x0b\n\x03\x61rg\x18\x01 \x01(\t\"\x07\n\x05\x45mpty\"\"\n\x0fGenericResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"b\n\x12RequestVoteRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61ndidateId\x18\x02 \x01(\x05\x12\x14\n\x0clastLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0blastLogTerm\x18\x04 \x01(\x05\"8\n\x13RequestVoteResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0bvoteGranted\x18\x02 \x01(\x08\"1\n\x05\x45ntry\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\x97\x01\n\x14\x41ppendEntriesRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08leaderId\x18\x02 \x01(\x05\x12\x14\n\x0cprevLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0bprevLogTerm\x18\x04 \x01(\x05\x12\x1e\n\x07\x65ntries\x18\x05 \x03(\x0b\x32\r.raftkv.Entry\x12\x14\n\x0cleaderCommit\x18\x06 \x01(\x05\"6\n\x15\x41ppendEntriesResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\x32\xd3\x02\n\rKeyValueStore\x12(\n\x08GetState\x12\r.raftkv.Empty\x1a\r.raftkv.State\x12*\n\x03Get\x12\x11.raftkv.StringArg\x1a\x10.raftkv.KeyValue\x12\x30\n\x03Put\x12\x10.raftkv.KeyValue\x1a\x17.raftkv.GenericResponse\x12$\n\x04ping\x12\r.raftkv.Empty\x1a\r.raftkv.Empty\x12\x46\n\x0brequestVote\x12\x1a.raftkv.RequestVoteRequest\x1a\x1b.raftkv.RequestVoteResponse\x12L\n\rappendEntries\x12\x1c.raftkv.AppendEntriesRequest\x1a\x1d.raftkv.AppendEntriesResponse2\xb4\x01\n\x08\x46rontEnd\x12$\n\x03Get\x12\x0e.raftkv.GetKey\x1a\r.raftkv.Reply\x12&\n\x03Put\x12\x10.raftkv.KeyValue\x1a\r.raftkv.Reply\x12*\n\x07Replace\x12\x10.raftkv.KeyValue\x1a\r.raftkv.Reply\x12.\n\tStartRaft\x12\x12.raftkv.IntegerArg\x1a\r.raftkv.ReplyB\x0bZ\t../raftkvb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\t../raftkv'
  _globals['_STATE']._serialized_start=22
  _globals['_STATE']._serialized_end=61
  _globals['_KEYVALUE']._serialized_start=63
  _globals['_KEYVALUE']._serialized_end=138
  _globals['_GETKEY']._serialized_start=140
  _globals['_GETKEY']._serialized_end=198
  _globals['_REPLY']._serialized_start=200
  _globals['_REPLY']._serialized_end=258
  _globals['_INTEGERARG']._serialized_start=260
  _globals['_INTEGERARG']._serialized_end=285
  _globals['_STRINGARG']._serialized_start=287
  _globals['_STRINGARG']._serialized_end=311
  _globals['_EMPTY']._serialized_start=313
  _globals['_EMPTY']._serialized_end=320
  _globals['_GENERICRESPONSE']._serialized_start=322
  _globals['_GENERICRESPONSE']._serialized_end=356
  _globals['_REQUESTVOTEREQUEST']._serialized_start=358
  _globals['_REQUESTVOTEREQUEST']._serialized_end=456
  _globals['_REQUESTVOTERESPONSE']._serialized_start=458
  _globals['_REQUESTVOTERESPONSE']._serialized_end=514
  _globals['_ENTRY']._serialized_start=516
  _globals['_ENTRY']._serialized_end=565
  _globals['_APPENDENTRIESREQUEST']._serialized_start=568
  _globals['_APPENDENTRIESREQUEST']._serialized_end=719
  _globals['_APPENDENTRIESRESPONSE']._serialized_start=721
  _globals['_APPENDENTRIESRESPONSE']._serialized_end=775
  _globals['_KEYVALUESTORE']._serialized_start=778
  _globals['_KEYVALUESTORE']._serialized_end=1117
  _globals['_FRONTEND']._serialized_start=1120
  _globals['_FRONTEND']._serialized_end=1300
# @@protoc_insertion_point(module_scope)
